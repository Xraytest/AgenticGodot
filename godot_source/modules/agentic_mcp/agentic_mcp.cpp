String raw_str = String::utf8((const char *)buf.ptr(), avail);
    Vector<String> lines = raw_str.split("\n");