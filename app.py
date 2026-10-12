"""
Bai thuc hanh Tuan 2 - Nhin thay entropy cua van ban
------------------------------------------------------
Flask backend: tu viet phan dem chu cai va tinh entropy (khong dung
collections.Counter hay thu vien thong ke co san), de ban thay ro
tung buoc tinh toan dang lam gi.
"""

import math
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
MAX_ENTROPY = math.log2(26)  # ~4.700439718... bit, dat duoc khi 26 chu cai deu nhau


def count_letters(text: str) -> list[int]:
    """
    Dem tan suat 26 chu cai a-z trong `text`.
    - Khong phan biet hoa/thuong (chuan hoa ve chu thuong).
    - Bo qua moi ky tu khong phai a-z (so, dau cau, khoang trang, ...).
    Tu viet bang vong lap thuong, KHONG dung collections.Counter,
    de ban nhin thay ro co che dem tung ky tu mot.
    """
    counts = [0] * 26
    for ch in text:
        c = ch.lower()
        if 'a' <= c <= 'z':
            idx = ord(c) - ord('a')
            counts[idx] += 1
    return counts


def entropy_bits(counts: list[int]) -> float:
    """
    Tinh entropy Shannon (don vi: bit) tu mang tan suat 26 chu cai.

        H = - sum( p_i * log2(p_i) )   voi p_i = count_i / tong_so_chu_cai

    Chu cai nao khong xuat hien (p_i = 0) duoc bo qua, vi theo quy uoc
    toan hoc 0 * log2(0) = 0 (gioi han).
    """
    total = sum(counts)
    if total == 0:
        return 0.0

    h = 0.0
    for c in counts:
        if c == 0:
            continue
        p = c / total
        h -= p * math.log2(p)
    return h


def caesar_encrypt(text: str, k: int) -> str:
    """
    Ma hoa Caesar: chi dich cac chu cai a-z/A-Z, giu nguyen ky tu khac.
    Cong thuc: chu_ma = (chu_ro + k) mod 26  (chi so 0..25, a=0, b=1, ...)
    """
    result = []
    for ch in text:
        if 'a' <= ch <= 'z':
            shifted = (ord(ch) - ord('a') + k) % 26
            result.append(chr(shifted + ord('a')))
        elif 'A' <= ch <= 'Z':
            shifted = (ord(ch) - ord('A') + k) % 26
            result.append(chr(shifted + ord('A')))
        else:
            result.append(ch)
    return ''.join(result)


@app.route('/')
def index():
    return render_template('index.html', max_entropy=round(MAX_ENTROPY, 4))


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(force=True) or {}
    text = data.get('text', '')
    try:
        k = int(data.get('k', 0)) % 26
    except (TypeError, ValueError):
        k = 0

    # --- Ban ro ---
    plain_counts = count_letters(text)
    plain_h = entropy_bits(plain_counts)

    # --- Ban ma Caesar (k) ---
    cipher_text = caesar_encrypt(text, k)
    cipher_counts = count_letters(cipher_text)
    cipher_h = entropy_bits(cipher_counts)

    return jsonify({
        'letters': list(ALPHABET),
        'plain_counts': plain_counts,
        'plain_entropy': round(plain_h, 4),
        'cipher_counts': cipher_counts,
        'cipher_entropy': round(cipher_h, 4),
        'max_entropy': round(MAX_ENTROPY, 4),
        'total_letters': sum(plain_counts),
        'k': k,
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
