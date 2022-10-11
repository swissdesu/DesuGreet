def role_was_added(memberBefore, memberAfter, role):
    """ checks wheter a specified role was added to the given member """
    memberBeforeEntrance = role in memberBefore.roles
    memberAfterEntrance = role in memberAfter.roles

    return not memberBeforeEntrance and memberAfterEntrance

def role_was_removed(memberBefore, memberAfter, role):
    """ checks wheter a specified role was removed from the given member """
    memberBeforeEntrance = role in memberBefore.roles
    memberAfterEntrance = role in memberAfter.roles

    return memberBeforeEntrance and not memberAfterEntrance