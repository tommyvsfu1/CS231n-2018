import numpy as np
from random import shuffle

def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """

  dW = np.zeros(W.shape) # initialize the gradient as zero

  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  # L_i = sigma(max(0,s_j-s_y_i + delta))
  loss = 0.0
  # dW_Transpose = C x D
  #dW_Transpose = dW.T
  for i in range(num_train):
    scores = X[i].dot(W) 
    correct_class_score = scores[y[i]]
    for j in range(num_classes):
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        # loss compute
        loss += margin
        # dW
        #dW_Transpose[j] += X[i]
        dW[:,j] += X[i,:]
        dW[:,y[i]] = dW[:,y[i]] - X[i]
        #dW_Transpose[y[i]] += (-X[i])

  dW = dW/num_train + 2 * reg * W
  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train

  # Add regularization to the loss.
  loss += reg * np.sum(W * W)

  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################

  return loss, dW


def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
  num_classes = W.shape[1]
  num_train = X.shape[0]
  # L_i = sigma(max(0,s_j-s_y_i + delta))
  loss = 0.0
  #for i in range(num_train):
  #  scores = X[i].dot(W)
  #  correct_class_score = scores[y[i]]
  
  scores = np.dot(X,W)  # NxC matrix
  '''
  debuging
  print("scores shape is",scores.shape)
  '''
  row_pick = np.arange(num_train) # Use Multi-dimensional indexing
  correct_class_score = scores[row_pick,y] # Nx1 vector
  
  #print("correct_class_score shape is",correct_class_score.shape)
  '''
    for j in range(num_classes):
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        loss += margin
  ''' 

  # step1 : broadcast the (correct_class_score + 1) vector
  # margin = N x C matrix
  correct_class_score_after = correct_class_score-1
  margin = (scores.T - correct_class_score_after.T).T
  #margin = scores - correct_class_score
  # step2 : bit-mask the matrix, pick the positive element 
  loss = (margin[margin>0].sum() - num_train)


  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train

  # Add regularization to the loss.
  loss += reg * np.sum(W * W)  
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################


  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
  # W = D x C
  # X = N x D
  # dW = D x C
  # dW.T = C x D
  # dW need to add the margin > 0 element
  # scores = N x C matrix
  # margin = N x C matrix
  dW_Transpose = dW.T
  margin_mask = (margin > 0)
  margin_mask_index = np.where(margin>0)
  #print("margin_mask_index",margin_mask_index)
  #print("len is",len(margin_mask_index[0]))
  # Use np.where to find margin_mask index
  # add first, include correct_class, deal with it later 
  #dW_Transpose[margin_mask_index[1]] = X[margin_mask_index[0]]
  for i in range(len(margin_mask_index[0])):
    dW_Transpose[margin_mask_index[1][i]] += X[margin_mask_index[0][i]]

  # deal with correct_class
  margin_mask_sum = np.sum(margin_mask,axis=1)
  #print("margin_mask",margin_mask)
  #print("margin_mask_sum",margin_mask_sum.shape)
  for i in range(margin_mask_sum.shape[0]):
    dW_Transpose[y[i]] -= margin_mask_sum[i]*X[i]

  dW = dW_Transpose.T/num_train + 2 * reg * W
  
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
