#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

__author__     = "olagino"
__email__      = "olaginos-buero@outlook.de"
__status__     = "Developement"

def handle(text, tiane, profile):
    tiane.say(text)
    tiane.end_Conversation()

def isValid(text):
    text = text.lower()
    if "sagen" in text and "säure" in text:
        return True
    return False
