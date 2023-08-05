from typing import Iterable, Optional, Sequence, Tuple

from . import ResponseCode
from ..primitives import ListP
from ..specials import SequenceSet
from ...bytes import MaybeBytes, BytesFormat

__all__ = ['Capability', 'PermanentFlags', 'UidNext', 'UidValidity', 'Unseen',
           'AppendUid', 'CopyUid']


class Capability(ResponseCode):
    """Lists the capabilities the server advertises to the client.

    Args:
        server_capabilities: The list of capabilities to advertise.

    """

    def __init__(self, server_capabilities: Iterable[MaybeBytes]) -> None:
        super().__init__()
        self.capabilities = [bytes(cap) for cap in server_capabilities]
        self._raw: Optional[bytes] = None

    def __contains__(self, capability: MaybeBytes) -> bool:
        return capability in self.capabilities

    @property
    def string(self) -> bytes:
        """The capabilities string without the enclosing square brackets."""
        if self._raw is not None:
            return self._raw
        self._raw = raw = BytesFormat(b' ').join(
            [b'CAPABILITY', b'IMAP4rev1'] + self.capabilities)
        return raw

    def __bytes__(self) -> bytes:
        return BytesFormat(b'[%b]') % self.string


class PermanentFlags(ResponseCode):
    """Indicates the permanent flags available in a mailbox.

    Args:
        flags: The flags to return.

    """

    def __init__(self, flags: Iterable[MaybeBytes]) -> None:
        super().__init__()
        self.flags: Sequence[MaybeBytes] = sorted(flags)
        self._raw = BytesFormat(b'[PERMANENTFLAGS %b]') % ListP(self.flags)

    def __bytes__(self) -> bytes:
        return self._raw


class UidNext(ResponseCode):
    """Indicates the next unique identifier value of the mailbox.

    Args:
        next_: The next available message UID.

    """

    def __init__(self, next_: int) -> None:
        super().__init__()
        self.next = next_
        self._raw = b'[UIDNEXT %i]' % next_

    def __bytes__(self) -> bytes:
        return self._raw


class UidValidity(ResponseCode):
    """Indicates the mailbox unique identifier validity value.

    Args:
        validity: The UID validity value.

    """

    def __init__(self, validity: int) -> None:
        super().__init__()
        self.validity = validity
        self._raw = b'[UIDVALIDITY %i]' % validity

    def __bytes__(self) -> bytes:
        return self._raw


class Unseen(ResponseCode):
    """Indicates the message sequence ID of the first message without the
    ``\\Seen`` flag.

    Args:
        next_: The sequence ID of the message.

    """

    def __init__(self, next_: int) -> None:
        super().__init__()
        self.next = next_
        self._raw = b'[UNSEEN %i]' % next_

    def __bytes__(self):
        return self._raw


class AppendUid(ResponseCode):
    """Indicates the newly assigned UIDs and UIDVALIDITY of messages appended
    to a mailbox.

    Args:
        validity: The UID validity value.
        uids: The UIDs of the appended messages.

    """

    def __init__(self, validity: int, uids: Iterable[int]) -> None:
        super().__init__()
        self.validity = validity
        self.uids = frozenset(uids)
        self._raw = BytesFormat(b'[APPENDUID %i %b]') \
            % (validity, SequenceSet.build(self.uids))

    def __bytes__(self) -> bytes:
        return self._raw


class CopyUid(ResponseCode):
    """Indicates the original and newly assigned UIDs and UIDVALIDITY of
    messages appended to the mailbox.

    Args:
        validity: The UID validity value.
        uids: The pairs of source UID mapped to destination UID.

    """

    def __init__(self, validity: int, uids: Iterable[Tuple[int, int]]) -> None:
        super().__init__()
        source_uids, dest_uids = zip(*uids)
        source_uid_set = SequenceSet.build(source_uids)
        dest_uid_set = SequenceSet.build(dest_uids)
        self._raw = b'[COPYUID %i %b %b]' \
            % (validity, bytes(source_uid_set), bytes(dest_uid_set))

    def __bytes__(self) -> bytes:
        return self._raw
