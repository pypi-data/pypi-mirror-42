============
Introduction
============

I created rzn because I'm used to running ``git push / pull`` for synchronizing my files. But for some use cases, like synchronizing my pictures / music etc, git would be an overkill in used storage and speed.

Rzn leverages rsync or rclone to synchronize your files. It searches for the configuration file ``.rzn`` in the current or parent directories like git so you can run ``rzn push / pull`` from any (sub)directory.


=======
Install
=======

::

   $ pip install git+https://github.com/meeuw/rzn

=====
Usage
=====

You can use the ``--backup`` argument of rsync / rclone to make sure rzn never overrides / deletes your files. You're free to use any directory but I use the following directory structure (local and remote):

::

   $ find bluh
   bluh/current/file1
   bluh/current/dir1/file1
   bluh/2019-03-03T07:31:09.015242/dir1/file1
   bluh/2019-03-04T09:10:08.023142/file2

As rzn doesn't do any versioning you'll have to be really cautious with cleaning your backups. As rsync also synchronizes your timestamps a tool like ``fdupes`` might be usefull to cleanup duplicate files. Before removing changed files I'd recommend to always compare the current and backupped files.

You can use ``sparsefilters`` to generate ``--filter`` arguments for rsync for sparse synchronisation. Sparse filters make it possible to only synchronize specific files / directories with a remote location.

The only required configuation item in the ``[main]`` section is ``remote``. The local location of the synchronisation arguments is determined by the location of your ``.rzn`` file.

Sample ``.rzn`` file:

::

  [main]
  remote = /home/meeuw/tmp/remote
  append = /current/
  sparsefilters =
     /bluh
     /dir***
  args = -Pa
    --backup
    --backup-dir={target}../{datetimeisoformat}
    --delete
    --delete-excluded


I recommend to always run ``rzn pull`` before making any changes to your files and ``rzn push`` as soon as possible.

::

  $ rzn pull

  $ vi file1

  $ rzn push

===
FAQ
===
Q: Why isn't the file which I've pushed shared anymore?
A: When using rclone you might not want to use a remote backup directory if your files are shared with other users, if you push changes to an existing file it will be replaced and your shared file will be moved to the backup directory. As (most) cloud remotes have their own versioning / recycle bin you don't need a backup dir. You can use the configuration item ``pull_args`` to use the ``--backup-dir`` argument only for your local files.

Q: Why should I use this tool instead of using automatic synchronisation?
A: Rzn gives you full control about when and how your files are synchronized.

Q: I've found a bug or limitation of rzn
A: Use the issue tracker (on GitHub) to report your issue and if you can, fix it yourself and submit a pull request.
