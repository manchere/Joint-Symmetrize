import maya.cmds as cmds
import re


class JointSymmetrize:

    def __init__(self):
        self.l_pref_name = ''
        self.r_pref_name = ''
        self.L_EXPR = '^[lL]([eE]+[fF]+[tT])?'
        self.R_EXPR = '^[rR]([iI]+[gG]+[hH]+[tT])?'

    def __hasPrefix(self, sel_joint, expr):
        return False if re.compile(expr).match(sel_joint) is None else True

    def __getPrefix(self, sel_joint, expr):
        if self.__hasPrefix(sel_joint, expr):
            return re.compile(expr).match(sel_joint).group()

    def __getRightSideJoint(self, l_jnt):
        for r_jnt in cmds.ls(type="joint"):
            r_check_pref = self.__getPrefix(r_jnt, self.R_EXPR)
            l_check_pref = self.__getPrefix(l_jnt, self.L_EXPR)
            if r_check_pref is not None:
                r_suf = r_jnt.replace(r_check_pref, '', 1)
                l_suf = l_jnt.replace(l_check_pref, '', 1)
                print(r_suf, l_suf)
                if r_suf == l_suf:
                    return r_jnt

    def symmetrize(self, joint_list):
        for cur_joint in joint_list:
            if self.__getRightSideJoint(cur_joint) is not None:
                cmds.connectAttr(cur_joint + '.translateZ', self.__getRightSideJoint(cur_joint) + '.translateZ',
                                 force=True)
                cmds.connectAttr(cur_joint + '.translateY', self.__getRightSideJoint(cur_joint) + '.translateY',
                                 force=True)

                cmds.shadingNode('multiplyDivide', asUtility=True, name='multiDivMirror')
                cmds.connectAttr(cur_joint + '.translateX', 'multiDivMirror.input1X')
                cmds.connectAttr(cur_joint + '.translateX', 'multiDivMirror.input1X')
                cmds.connectAttr('multiDivMirror.output1X', self.__getRightSideJoint(cur_joint) + '.translateX')

    def removeSymmetrize(self):
        pass


if cmds.window('Joint_Symmetrize', exists=True):
    cmds.deleteUI('Joint_Symmetrize')

cmds.window('Joint_Symmetrize', title='Joint Symmetrize', w=200)
sym = JointSymmetrize()
cmds.rowColumnLayout(rowSpacing=(20, 20), numberOfColumns=2)
cmds.frameLayout(label='Options', cll=False, cl=True, bgc=[0.2, 0.2, 0.2], w=200)
cmds.button(label="Symmetrize", bgc=[0, 0.2, 0.3], command=lambda x: sym.symmetrize(cmds.ls(sl=True, type="joint")),
            w=200)
cmds.button(label="Remove Symmetrize", bgc=[0.5, 0, 0], command=lambda x: '', w=200)
cmds.showWindow()
