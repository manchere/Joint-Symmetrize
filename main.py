import maya.cmds as cmds
import re


class JointSymmetrize:

    def __init(self):
        self.SymmetricInfo = []
        self.left_Expr = '^[lL]([eE]+[fF]+[tT])?'
        self.right_Expr = '^[rR]([iI]+[gG]+[hH]+[tT])?'


    def matchingJoint(self, obj):
        self.symmetricInfo[0] = re.compile(self.left_Expr).match(obj).group()
        self.symmetricInfo[1] = re.compile(self.right_Expr).match(obj).group()
        return self.symmetricInfo[0], self.symmetricInfo


    def symmetrize(self, jointList):
        for cur_joint in jointList:
            if matchingJoint(cur_joint, self.left_Expr):
                t = matchingJoint(self.right_Expr)

                cmds.connectAttr(cur_joint + '.translateZ', cur_joint + '.translateZ', force=True)
                cmds.connectAttr(cur_joint + '.translateY', cur_joint + '.translateY', force=True)

                cmds.shadingNode('multiplyDivide', asUtility=True, name='MultiDivMirror')
                cmds.connectAttr(cur_joint + '.translateX', 'MultiDivMirror.input1X')
                cmds.connectAttr(cur_joint + '.translateX', 'MultiDivMirror.input1X')
                cmds.connectAttr('MultiDivMirror.output1X', cur_joint + '.translateX')


    def removeSymmetrize():
        pass