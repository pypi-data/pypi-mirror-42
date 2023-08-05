============
Chainer Hajo
============

Chainer Hajo provides utility classes
to be used with the excellent Chainer framework
which are shared across projects here at hajo.me.

In particular, this package includes the following helpers:

* ``WriteImage`` allows one to report image arrays
   to the chainer reporting system as an observation
   and to write those to disk as image files.
   Enabled using optional parameters, ``WriteImage`` can also display
   the image inside an IPython environment, such as Jupyter notebooks.
   Together with ``SecondTrigger`` this allows to show the user
   regular previews of the training progress
   while the associated Jupyter notebook is running.

* ``PrintNoLog`` will print a set of observations,
   such as the current loss values, to the command line
   without storing them into a file and/or serializing the history to JSON.
   For projects with fast training iterations and large epochs,
   this can greatly increase training speed by reducing disk IO.

* ``SecondTrigger`` and ``MinuteTrigger`` are trigger objects
   which will fire
   independently of the number of iterations and epochs,
   but at a fixed rate such as once per 30 seconds.
   This is useful for providing continuous diagnostics
   and performance output for long-running training sessions,
   while keeping the evaluation overhead constant.
   When using triggers that operate on the iteration or epoch,
   then adjusting the number of items per training batch
   would increase or reduce the duration per iteration,
   thus making it necessary to adjust the trigger timings.
   These triggers avoid such problems
   by triggering based on the wall clock time.

* ``LogHyperparameter`` is a trainer extension
   which will copy the current value of a hyperparameter
   over into an reporting observation.
   This is useful for graphing or logging the training rate,
   if modified with ``ExponentialShift`` or ``LinearShift``.

* ``ClassifyModify`` and the associated ``ClassifyModifyChain``
   will repeatedly modify the data array with ``x += conv_b(Elu(conv_a(x)))``
   which has proven to be an excellent model for learn-able residuals
   for video, image and sound data processing.
   ``ClassifyModifySequence`` further generalizes this
   by allowing the user to specify varying kernel size,
   stride, padding, and dilation parameters for the different iterations.

* ``SynthAndGate`` is a reusable generator Chain
   which will convolve the input signal and then calculate
   the sigmoid-gated sums of tanh generators.
   Usually, the input signal is upsampled to multiple tanh channels
   per output element, which allows this operator to use the gating
   for choosing between different generators for each output plane.
   This approach has proven to work well for many different
   likelihood modeling tasks, e.g. generating the distribution
   for a ``F.softmax_cross_entropy`` loss.
   Optionally, the limiting by tanh can be disabled.
   This has proven useful for modeling time-continuous image streams,
   e.g. videos or continuous EEG signals.


------------
Coming soon:
------------

* ``Discretizer`` and the accompanying ``discretize`` function
   can be used to reduce continuous multi-direction vectors
   to a limited number of discrete directions,
   while optionally enforcing a given vector norm.
