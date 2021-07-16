import argparse
from difflib import get_close_matches as match
from . import Imgflip, Box

def error(*msg):
    print(*msg)
    raise SystemExit()

def list_to_box(list_box):
    text = list_box[0]
    pos = (int(list_box[1]), int(list_box[2]))
    size = (int(list_box[3]), int(list_box[4]))
    color = list_box[5] if list_box[5] != "_" else "#ffffff"
    o_color = list_box[6] if list_box[6] != "_" else "#000000"
    return Box(text, pos, size, color, o_color)

parser = argparse.ArgumentParser(
    description="Command line interface for imgflip.py", 
    prog="imgflip.py"
)

parser.add_argument(
    "-v", 
    "--version", 
    action="version", 
    version="imgflip.py 1.0"
)


parser.add_argument(
    "-pm",
    "--popular-memes",
    dest="popular_memes",
    action="store_true",
    help="Get the top 100 popular memes"
)

parser.add_argument(
    "-u",
    "--username",
    dest="username",
    help="Your imgflip username"
)

parser.add_argument(
    "-p",
    "--password",
    dest="password",
    help="Your imgflip password"
)

parser.add_argument(
    "-tid", 
    "--template-id", 
    metavar="ID",
    dest="template_id",
    type=int, 
    help="The template id. Not to be used with -tname"
)

parser.add_argument(
    "-tname", 
    "--template-name", 
    metavar="NAME", 
    dest="template_name",
    help="The name of one of the top 100 popular memes. "
    + "Not to be used with -tid"
)

parser.add_argument(
    "-top",
    "--top-text",
    "-ft",
    "--first-text",
    metavar="TEXT",
    dest="top_text",
    help="The text of the first box in the meme"
)

parser.add_argument(
    "-bot",
    "--bottom-text",
    "-s",
    "-second-text",
    metavar="TEXT",
    dest="bottom_text",
    help="The text of the second box in the meme"
)

parser.add_argument(
    "--box",
    nargs=7,
    metavar=(
        "TEXT", 
        "XPOS", 
        "YPOS", 
        "WIDTH", 
        "HEIGHT", 
        "TEXT_COLOR", 
        "TEXT_OUTLINE_COLOR"
    ),
    dest="boxes",
    action="append",
    help="A text box to be used on the meme. "
    + "For text_color and text_outline_color use '_' if you want to "
    + "use the default value (#ffffff and #000000 respectively)"
)

parser.add_argument(
    "-f",
    "--font",
    dest="font",
    help="The font for the text on the meme. Must be impact or arial. "
    + " Defaults to impact"
)

parser.add_argument(
    "-fs",
    "--font-size",
    dest="max_font_size",
    type=int,
    help="The max font size. Defaults to 50."
)

args = parser.parse_args()

if args.popular_memes:
    memes = Imgflip("_", "_").popular_memes(dictionary=False)
    print("\n".join(
        f"""{meme.name}
        id: {meme.id}
        url: {meme.url}
        """ for meme in memes
    ))

else:
    username = args.username
    password = args.password

    if username is None:
        error("Username missing!")
        
    if password is None:
        error("Password missing!")
    
    client = Imgflip(username, password)
    template_id = args.template_id

    if template_id is None:
        if args.template_name is None:
            error("template-id or template-name must be passed.")
        template_name = args.template_name.lower()
        memes = {
            template.name.lower(): template.id 
            for template in client.popular_memes(dictionary=False)
        }
        if template_name not in list(memes):
            close_match = match(args.template_name, list(memes), 1)
            out = f"Template '{args.template_name}' not found."
            if len(close_match) != 0:
                out += f" Did you mean '{close_match[0]}'?"
            error(out)
        template_id = memes[template_name]
    
    if not any((args.top_text, args.bottom_text, args.boxes)):
        error("No text provided.")
    else:
        max_font_size = 50
        if args.max_font_size is not None:
            max_font_size = args.max_font_size
        font = "impact"
        if args.font is not None:
            font = args.font
        boxes = None
        if args.boxes is not None:
            boxes = [list_to_box(box) for box in args.boxes]
        meme = client.make_meme(
            template_id, 
            font, 
            max_font_size, 
            args.top_text, 
            args.bottom_text, 
            boxes
        )
        print(
            f"""meme created!
            You can find it at: {meme.page_url}
            Image link: {meme.url}
            """.replace("  ", "")
        )