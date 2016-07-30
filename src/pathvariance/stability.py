"""Stability verdict with an explicit minimum-run-count gate.

Three runs cannot describe a distribution. With so few samples, one path taking
two of three runs looks like 67 percent stability, but the confidence interval
around that is so wide that the number misleads more than it informs. So this
module refuses to issue entropy or a verdict below a minimum run count and says
why, rather than printing a figure that reads as authoritative.

The verdict compares the modal share against a declared threshold. At or above
