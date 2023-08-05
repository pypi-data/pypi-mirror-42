env2fs: write env vars to filesystem (CI tool)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

env2fs is a quick CLI to write environment variables content to the file
system.

Example usage::

   env2fs write SSH_PRIVATE_KEY $HOME/.ssh/id_ed25519 mode=0600

This will write the content of the ``$SSH_PRIVATE_KEY`` env var into
``$HOME/.ssh/id_ed2551`` and set the access permission to ``0600``.

Any parent directory it would have to create, such as ``$HOME/.ssh`` in a CI
environment, will be created with the same permissions, except with the execute
bit in addition to every read bit, to allow directory traversal.

That's it ! Run ``env2fs`` to get help for all commands.
