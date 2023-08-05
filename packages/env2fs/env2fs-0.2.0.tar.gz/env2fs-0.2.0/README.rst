env2fs: write env vars to filesystem (CI tool)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Write a file with an env var content or a set of env vars.

Usage example::

    env2fs ~/.ssh/id_rsa SSH_KEY fmod=600 dmod=700

Note that the missing dollar sign is intendent to prevent evaluation from
the parent shell itself.

The above example writes the contents of the ``$SSH_KEY`` environment variable
into ``~/.ssh/id_rsa``, with a mode of 600 and 700 for any parent directory
that will be automatically created if necessary.

To write an env file, pass a variable name that ends with underscore, ie::

    export staging_pgpass=foo
    env2fs staging.env staging_

Will write staging.env with contents::

    pgpass=foo

Extra CLI options::

  --dryrun       Do not actually touch the fs
  --verbose,-v      Verbose output
