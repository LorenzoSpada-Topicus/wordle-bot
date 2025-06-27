def check_len(string, req_length):
    if len(string) != req_length:
        print(f"didnt enter {req_length} character word")
        return False
    return True