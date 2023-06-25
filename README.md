# ControlAccess
User data management for Control Access.

This program provides the data management for Control Access device.

Data Base structure:

        Data Base: Users
    Tables:

        UserInfo Columns:
    UserName        varchar(50)
    RegisterCURP    varchar(50)
    CareerAddress   varchar(50)
    UserType        varchar(50)
    Status          varchar(50)

        UserAccess Columns:
    Date            varchar(50)
    UserName        varchar(50)
    UserType        varchar(50)
    Action          varchar(50)