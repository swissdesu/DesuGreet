class SameMemberComparator:
    def __init__(self, memberBefore, memberAfter) -> None:
        self.memberBefore = memberBefore
        self.memberAfter = memberAfter

    def roleWasAdded(self, role):
        memberBeforeEntrance = role in self.memberBefore.roles
        memberAfterEntrance = role in self.memberAfter.roles

        return not memberBeforeEntrance and memberAfterEntrance

    def roleWasRemoved(self, role):
        memberBeforeEntrance = role in self.memberBefore.roles
        memberAfterEntrance = role in self.memberAfter.roles

        return memberBeforeEntrance and not memberAfterEntrance