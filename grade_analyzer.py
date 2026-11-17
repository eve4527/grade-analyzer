import csv
import json


def load_scores(filename):
    """读取 CSV,返回 (学生列表, 跳过的行数)"""
    students = []
    skipped = 0

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                math = float(row["math"])
                english = float(row["english"])
            except (ValueError, KeyError):
                skipped += 1
                continue

            students.append({
                "name": row["name"],
                "math": math,
                "english": english,
            })

    return students, skipped


def analyze(students):
    """计算统计量,返回统计字典"""
    if not students:
        return {
            "count": 0,
            "math_avg": 0,
            "english_avg": 0,
            "top": None,
            "bottom": None,
            "students": [],
        }

    enriched = []
    for s in students:
        avg = (s["math"] + s["english"]) / 2
        enriched.append({
            "name": s["name"],
            "math": s["math"],
            "english": s["english"],
            "average": avg,
        })

    count = len(enriched)
    math_total = 0
    english_total = 0
    for s in enriched:
        math_total += s["math"]
        english_total += s["english"]

    top = enriched[0]
    bottom = enriched[0]
    for s in enriched:
        if s["average"] > top["average"]:
            top = s
        if s["average"] < bottom["average"]:
            bottom = s

    return {
        "count": count,
        "math_avg": math_total / count,
        "english_avg": english_total / count,
        "top": {"name": top["name"], "average": top["average"]},
        "bottom": {"name": bottom["name"], "average": bottom["average"]},
        "students": enriched,
    }


def print_report(stats):
    """打印给人看的报告"""
    print("=" * 30)
    print("成绩报告")
    print("=" * 30)

    if stats["count"] == 0:
        print("没有有效数据")
        return

    print(f"有效学生数:{stats['count']}")
    print()

    ordered = sorted(stats["students"], key=lambda s: s["average"], reverse=True)
    for s in ordered:
        print(f"{s['name']}: 数学 {s['math']:.1f}, 英语 {s['english']:.1f}, 平均 {s['average']:.1f}")

    print()
    print(f"数学平均:{stats['math_avg']:.1f}")
    print(f"英语平均:{stats['english_avg']:.1f}")
    print(f"最高:{stats['top']['name']}({stats['top']['average']:.1f})")
    print(f"最低:{stats['bottom']['name']}({stats['bottom']['average']:.1f})")
    print("=" * 30)


def save_json(data, filename):
    """把数据保存成 JSON 文件"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    try:
        students, skipped = load_scores("scores.csv")
    except FileNotFoundError:
        print("找不到 scores.csv,请确认文件在当前目录")
        return

    if skipped > 0:
        print(f"注意:跳过了 {skipped} 行无效数据")

    stats = analyze(students)
    print_report(stats)

    if stats["count"] > 0:
        save_json(stats, "results.json")
        print("报告已保存到 results.json")


if __name__ == "__main__":
    main()