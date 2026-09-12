import sys
import jieba

def get_words(text: str):
    """分词，去掉空白符号"""
    words = jieba.lcut(text)
    res = []
    for w in words:
        w = w.strip()
        if len(w) > 0:
            res.append(w)
    return res

def calc_simhash(words, hash_bits=64):
    """简单simhash实现"""
    import hashlib
    v = [0] * hash_bits
    for word in words:
        h = hashlib.sha256(word.encode("utf-8")).hexdigest()
        h_int = int(h, 16)
        for i in range(hash_bits):
            bit = (h_int >> i) & 1
            if bit:
                v[i] += 1
            else:
                v[i] -= 1
    # 生成指纹
    fingerprint = 0
    for i in range(hash_bits):
        if v[i] > 0:
            fingerprint |= (1 << i)
    return fingerprint

def hamming_distance(h1, h2):
    """计算汉明距离"""
    return bin(h1 ^ h2).count("1")

def calc_similarity(text1, text2):
    words1 = get_words(text1)
    words2 = get_words(text2)
    if len(words1) == 0 or len(words2) == 0:
        return 0.0
    hash1 = calc_simhash(words1)
    hash2 = calc_simhash(words2)
    dist = hamming_distance(hash1, hash2)
    similarity = 1.0 - dist / 64
    return round(similarity, 2)

def main():
    # 命令行参数：main.py 原文路径 抄袭路径 输出文件路径
    if len(sys.argv) != 4:
        print("参数错误！用法：python main.py orig.txt add.txt ans.txt")
        return
    orig_path = sys.argv[1]
    copy_path = sys.argv[2]
    out_path = sys.argv[3]
    try:
        with open(orig_path, "r", encoding="utf-8") as f:
            orig_text = f.read()
        with open(copy_path, "r", encoding="utf-8") as f:
            copy_text = f.read()
    except FileNotFoundError:
        print("文件不存在")
        return
    except Exception as e:
        print(f"读取异常：{e}")
        return
    rate = calc_similarity(orig_text, copy_text)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"{rate:.2f}")

if __name__ == "__main__":
    main()
