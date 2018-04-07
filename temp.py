#!/usr/bin/env python
# -*- coding: utf-8 -*-


if __name__ == "__main__":
    y = Yolo(100)
    print(y.age)
    y.jeSuis_ici = "toto"
    print(y.jeSuis_ici)
    print(y.__dict__)