# -*- coding: utf-8 -*-

# Original views
from basic.base.views import InfoList, InfoCreate, InfoDetail, InfoEdit, InfoDelete


class InfoListB1(InfoList):
    appname = "base2"
    modelname = "info"


class InfoCreateB1(InfoCreate):
    pass


class InfoDetailB1(InfoDetail):
    pass


class InfoEditB1(InfoEdit):
    pass


class InfoDeleteB1(InfoDelete):
    pass


class InfoListB2(InfoList):
    appname = "base2"
    modelname = "info2"


class InfoCreateB2(InfoCreate):
    pass


class InfoDetailB2(InfoDetail):
    pass


class InfoEditB2(InfoEdit):
    pass


class InfoDeleteB2(InfoDelete):
    pass
