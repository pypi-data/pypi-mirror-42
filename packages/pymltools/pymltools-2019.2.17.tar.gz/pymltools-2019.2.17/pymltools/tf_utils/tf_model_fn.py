# -*- coding:utf-8 -*-
from __future__ import absolute_import

import logging

import tensorflow as tf

from .project_demo import OptimizerType
from .triplet_loss import batch_hard_triplet_loss

End_Point_Prediction_Key = "prediction_keys"
Prediction_Key_Class = "class"
Prediction_Key_Prob = "prob"


def tf_triplet_loss_model_fn(network, scope_name: str, features_embedding_key: str, features_filename_key: str,
                             get_learning_rate_func, optimizer_type: OptimizerType = OptimizerType.adam,
                             logger=logging, use_l2_normalize: bool = False):
    """

    Args:
        network: func, like func(scope_name, features, params, is_training)
        scope_name: str, scope name of net
        features_embedding_key: str, key
        features_filename_key: str, key
        get_learning_rate_func: func, get learning rate
        optimizer_type: OptimizerType
        logger: logging.Logger
        use_l2_normalize: bool, whether to use l2 before embeddings. Facenet use this.

    Returns:
        func: model fn for estimator
    """

    def model_func(features, labels, mode, params):
        if labels is not None:
            labels = tf.cast(labels, tf.int64)

        if mode == tf.estimator.ModeKeys.TRAIN:
            embeddings, end_points = network(scope_name=scope_name, features=features, params=params, labels=labels,
                                             is_training=True)
        else:
            embeddings, end_points = network(scope_name=scope_name, features=features, params=params, labels=labels,
                                             is_training=False)

        embedding_mean_norm = tf.reduce_mean(tf.norm(embeddings, axis=1))
        tf.summary.scalar("embedding_mean_norm", embedding_mean_norm)

        # √ axis = 0: means normalize each dim by info from this batch
        # √ axis = 1: means normalize x each dim only by x info ; 单位向量
        # todo google facenet use tf.nn.l2_normalize(embeddings, axis=1) in papers
        # 1) 单位向量, margin, 无法容纳足够多的聚类中心
        # 2) github项目, 没有使用单位向量
        if use_l2_normalize:
            embeddings = tf.nn.l2_normalize(embeddings, axis=0)  # todo 不合理

        if mode == tf.estimator.ModeKeys.PREDICT:
            predictions = {
                features_embedding_key: embeddings,
                features_filename_key: features[features_filename_key]
            }
            if End_Point_Prediction_Key in end_points:
                predictions.update(end_points[End_Point_Prediction_Key])
            return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

        # Define triplet loss
        loss = batch_hard_triplet_loss(labels, embeddings, margin=params.margin, squared=False)

        with tf.variable_scope("metrics"):
            eval_metric_ops = {"embedding_mean_norm": tf.metrics.mean(embedding_mean_norm)}

        if mode == tf.estimator.ModeKeys.EVAL:
            return tf.estimator.EstimatorSpec(mode, loss=loss, eval_metric_ops=eval_metric_ops)

        # Summaries for training
        tf.summary.scalar('loss', loss)

        # Define training step that minimizes the loss with the Adam optimizer
        if optimizer_type == OptimizerType.sgd:
            optimizer = tf.train.GradientDescentOptimizer(learning_rate=get_learning_rate_func())
        else:
            optimizer = tf.train.AdamOptimizer(learning_rate=get_learning_rate_func())

        # train op
        update_op_list = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        logger.debug("update ops: {}".format(update_op_list))
        if update_op_list:
            # batch norm need this code:
            with tf.control_dependencies(update_op_list):
                train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())
        else:
            train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())

        return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op)

    return model_func


def tf_softmax_model_fn(network, scope_name: str, get_learning_rate_func, features_filename_key: str = None,
                        optimizer_type: OptimizerType = OptimizerType.adam, logger=logging):
    """

    Args:
        network: func,
        scope_name: str, scope name of net
        features_filename_key: str, key
        get_learning_rate_func: func, get learning rate
        optimizer_type: OptimizerType
        logger: logging.Logger

    Returns:
        func: model fn for estimator
    """

    def model_func(features, labels, mode, params):
        if labels is not None:
            labels = tf.cast(labels, tf.int64)

        if mode == tf.estimator.ModeKeys.TRAIN:
            logits, end_points = network(scope_name=scope_name, features=features, params=params, labels=labels,
                                         is_training=True)
        else:
            logits, end_points = network(scope_name=scope_name, features=features, params=params, labels=labels,
                                         is_training=False)

        predicted_classes = tf.argmax(logits, 1)
        if mode == tf.estimator.ModeKeys.PREDICT:
            predictions = {
                Prediction_Key_Class: predicted_classes,
                Prediction_Key_Prob: tf.nn.softmax(logits),
            }
            if features_filename_key:
                predictions[features_filename_key] = features[features_filename_key]

            if End_Point_Prediction_Key in end_points:
                predictions.update(end_points[End_Point_Prediction_Key])
            return tf.estimator.EstimatorSpec(mode, predictions=predictions)

        # Compute loss.
        loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

        # Create training op.
        if mode == tf.estimator.ModeKeys.TRAIN:
            tf.summary.scalar('loss', loss)

            # Define training step that minimizes the loss with the Adam optimizer
            if optimizer_type == OptimizerType.sgd:
                optimizer = tf.train.GradientDescentOptimizer(learning_rate=get_learning_rate_func())
            else:
                optimizer = tf.train.AdamOptimizer(learning_rate=get_learning_rate_func())

            # train op
            update_op_list = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            logger.debug("update ops: {}".format(update_op_list))
            if update_op_list:
                # batch norm need this code:
                with tf.control_dependencies(update_op_list):
                    train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())
            else:
                train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())

            return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op, scaffold=None)

        # Compute evaluation metrics.
        eval_metric_ops = {'accuracy': tf.metrics.accuracy(labels=labels, predictions=predicted_classes)}
        return tf.estimator.EstimatorSpec(mode, loss=loss, eval_metric_ops=eval_metric_ops)

    return model_func


def tf_margin_base_softmax_model_fn(network, loss_fn, scope_name: str, get_learning_rate_func,
                                    optimizer_type: OptimizerType = OptimizerType.adam, logger=logging):
    """

    Args:
        network: func,
        loss_fn: func,
        scope_name: str, scope name of net
        get_learning_rate_func: func, get learning rate
        optimizer_type: OptimizerType
        logger: logging.Logger

    Returns:
        func: model fn for estimator
    """

    def model_func(features, labels, mode, params):
        if labels is not None:
            labels = tf.cast(labels, tf.int64)

        if mode == tf.estimator.ModeKeys.TRAIN:
            embeddings, end_points = network(scope_name=scope_name, features=features, params=params, labels=labels,
                                             is_training=True)
        else:
            embeddings, end_points = network(scope_name=scope_name, features=features, params=params, labels=labels,
                                             is_training=False)

        logits, loss = loss_fn(embeddings=embeddings, labels=labels, )
        predicted_classes = tf.argmax(logits, 1)
        if mode == tf.estimator.ModeKeys.PREDICT:
            predictions = {
                Prediction_Key_Class: predicted_classes,
                Prediction_Key_Prob: tf.nn.softmax(logits),
            }
            if End_Point_Prediction_Key in end_points:
                predictions.update(end_points[End_Point_Prediction_Key])
            return tf.estimator.EstimatorSpec(mode, predictions=predictions)

        # Create training op.
        if mode == tf.estimator.ModeKeys.TRAIN:
            tf.summary.scalar('loss', loss)

            # Define training step that minimizes the loss with the Adam optimizer
            if optimizer_type == OptimizerType.sgd:
                optimizer = tf.train.GradientDescentOptimizer(learning_rate=get_learning_rate_func())
            else:
                optimizer = tf.train.AdamOptimizer(learning_rate=get_learning_rate_func())

            # train op
            update_op_list = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            logger.debug("update ops: {}".format(update_op_list))
            if update_op_list:
                # batch norm need this code:
                with tf.control_dependencies(update_op_list):
                    train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())
            else:
                train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())

            return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op, scaffold=None)

        # Compute evaluation metrics.
        eval_metric_ops = {'accuracy': tf.metrics.accuracy(labels=labels, predictions=predicted_classes)}
        return tf.estimator.EstimatorSpec(mode, loss=loss, eval_metric_ops=eval_metric_ops)

    return model_func


__all__ = ("tf_triplet_loss_model_fn", "tf_softmax_model_fn", "End_Point_Prediction_Key",
           "tf_margin_base_softmax_model_fn", "Prediction_Key_Prob", "Prediction_Key_Class")
