def to_halfwidth(query: str) -> str:
    """Convert the query string to halfwidth

    全形字符 unicode 編碼從 65281 ~ 65374(十六進制 0xFF01 ~ 0xFF5E)
    半形字符 unicode 編碼從 33 ~ 126(十六進制 0x21~ 0x7E)
    空格比較特殊, 全形為12288(0x3000), 半形為32(0x20)
    而且除空格外, 全形/半形按 unicode 編碼排序在順序上是對應的
    所以可以直接通過用+-法來處理非空格字元, 對空格單獨處理.
    """
    rstring = ""
    for char in query:
        code = ord(char)
        if code == 0x3000:
            code = 0x0020
        else:
            code -= 0xFEE0
        if code < 0x0020 or code > 0x7E:  # fallback check
            rstring += char
        else:
            rstring += chr(code)
    return rstring
