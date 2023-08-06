"""
A user-friendly kubectl wrapper for interacting with pods.

Common labels are automatically aliased - using 'name=example' will try
'app.kubernetes.io/name=example' if the original selector doesn't match any pods.

Tail logs from the first pod matching 'app.kubernetes.io/name=service':

\b
    katie logs name=service

Run a command in the first pod matching 'app.kubernetes.io/name=service':

\b
    katie exec name=service -- sh
"""

__author__ = 'Sam Clements <sam@borntyping.co.uk>'
__version__ = '0.2.0'
