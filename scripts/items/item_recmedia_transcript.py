import os
from tqdm import tqdm
from scripts.objects.recorded_media import RecMedia
from scripts.core.file_loading import write_file
from scripts.core.constants import ITEM_DIR, PBAR_FORMAT
from scripts.utils import echo, media_helper, util


def process_rm(rm: RecMedia):
    icon = "cd" if rm.category == "CDs" else "vhs"

    content = []

    content.append("{{Transcript")
    content.append(f"|icon={icon}")
    content.append("|text=")

    prev_speaker = None
    for speaker, line in rm.get_speaker_lines():
        if line.codes:
            icons = []

            for code, value in line.codes.items():
                icon = media_helper.get_icon(code, value=value, size="24px")
                value_text = util.format_positive(value)

                if icon:
                    icons.append(f"{icon}<small>''{value_text}''</small>")
                else:
                    # Fallback for recipes
                    name = media_helper.get_code_name(code)
                    if "%1" in name:
                        name = name.replace("%1", str(value_text))
                    icons.append(f"''<small>{name}</small>''")

            icon_text = " ".join(icons)
            line_text = f"{line.text} {icon_text}"

            # Wrap * in <code> to avoid dotpoints
            if line_text.startswith("*"):
                line_text = line_text.replace("*", "<nowiki>*</nowiki>", 1)
        else:
            line_text = line.text


        if prev_speaker != speaker:
            if prev_speaker is not None:
                content.append("}}")
            content.append("{{Transcript/row|" + speaker + "|" + line_text + "<br>")
        else:
            content.append(line_text + "<br>")
        prev_speaker = speaker
    
    if prev_speaker is not None:
        content.append("}}")

    content.append("}}")

    return content


def main(batch=False):
    """
    Generate recorded media transcripts.

    Args:
        batch (bool): If True, skip language loading (for batch processing).
    """
    from scripts.core.language import Language
    if not batch:
        Language.get() #pre-init language

    root_path = os.path.join(ITEM_DIR, "recorded_media", "transcripts")

    with tqdm(total=RecMedia.count(), desc="Generating recmedia transcripts", bar_format=PBAR_FORMAT, unit=" recmedia", leave=False) as pbar:
        for rm_id, rm in RecMedia.all().items():
            pbar.set_postfix_str(f"Processing: {rm.name[:50]}")

            content = process_rm(rm)

            file_name = (f"{rm_id}.txt")
            write_file(content, rel_path=file_name, root_path=root_path, suppress=True)

            pbar.update(1)
    
    echo.success(f"Generated {RecMedia.count()} recorded media transcripts: '{root_path.format(language_code=Language.get())}'")


if __name__ == "__main__":
    main()