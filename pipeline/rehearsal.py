from .storyboard import ROOT, load_storyboard


def format_time(seconds: int) -> str:
    minutes, remainder = divmod(seconds, 60)
    return f"{minutes:02d}:{remainder:02d}"


def rehearsal_sheet(storyboard: dict) -> str:
    start = 0
    lines = [storyboard["title"], ""]
    for shot in storyboard["shots"]:
        duration = shot["duration_seconds"]
        end = start + duration
        lines.append(f"{format_time(start)}–{format_time(end)}  {shot['id']} ({duration}s)")
        narration = shot["narration"]
        if narration is None:
            lines.append("  [No narration]")
        else:
            lines.extend((f"  {narration['text']}", f"  EN: {narration['subtitle_en']}"))
        lines.append("")
        start = end
    return "\n".join(lines)


def main() -> None:
    try:
        storyboard = load_storyboard(ROOT / "storyboard.json")
    except (OSError, ValueError) as error:
        raise SystemExit(f"Invalid storyboard: {error}") from None
    print(rehearsal_sheet(storyboard))


if __name__ == "__main__":
    main()
