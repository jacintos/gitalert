#! /usr/bin/env python

from optparse import OptionParser
import git, netgrowl, os, socket, sys

PASSWORD = None


def main():
    parser = OptionParser()
    parser.add_option('-r', '--repo', dest='repo', metavar='DIR', help='Path to repository')
    parser.add_option('-c', '--commit', dest='commit', action='store_true', default=True, help='Notify of a commit')
    parser.add_option('-p', '--push', dest='commit', action='store_false', help='Notify of a push to remote repository')
    opts, args = parser.parse_args()

    if opts.repo is None:
        print 'Specify path to Git repository'
        return 1

    if opts.repo[-1] == os.path.sep:
        opts.repo = opts.repo.rstrip(os.path.sep)

    try:
        repo = git.Repo(opts.repo)
    except git.errors.NoSuchPathError:
        print 'Repository does not exist at %s' % opts.repo
        return 2

    head = repo.heads[0]
    commit = head.commit
    committer = commit.committer.name

    if opts.commit is True:
        subject = commit.message

        title = os.path.basename(opts.repo)
        description = "%s committed: '%s'" % (committer, subject)
    else:
        title = os.path.basename(opts.repo)
        description = "%s pushed to central repository" % (committer)

    addr = '255.255.255.255', netgrowl.GROWL_UDP_PORT

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Register notification
    p = netgrowl.GrowlRegistrationPacket(application='gitalert', password=PASSWORD)
    p.addNotification()
    s.sendto(p.payload(), addr)

    # Send notification
    p = netgrowl.GrowlNotificationPacket(application='gitalert',
                                         title=title,
                                         description=description,
                                         password=PASSWORD)
    s.sendto(p.payload(), addr)

    s.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
