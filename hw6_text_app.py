from hw6_texticular import Textastic
from hw6_parser import lyrics_parser
import os

def main():
    # textastic framework
    tt = Textastic()

    # load txt files with lyrics
    lyrics_files = [
        ('St. Chroma', 'hw6_p1'),
        ('Rah Tah Tah', 'hw6_p2'),
        ('Noid', 'hw6_p3'),
        ('Darling, I', 'hw6_p4'),
        ('Hey Jane', 'hw6_p5'),
        ('I Killed You', 'hw6_p6'),
        ('Judge Judy', 'hw6_p7'),
        ('Sticky', 'hw6_p8'),
        ('Take Your Mask Off', 'hw6_p9'),
        ('Tomorrow', 'hw6_p10'),
        ('Thought I Was Dead', 'hw6_p11'),
        ('Like Him', 'hw6_p12'),
        ('Balloon', 'hw6_p13'),
        ('I Hope You Find Your Way Home', 'hw6_p14')
    ]

    for title, file in lyrics_files:
        print(f"Label {file} as {title}...")
        tt.load_text(file, label=title, parser=lyrics_parser)

    # visualizations!
    print("Generating Sankey diagram...")
    tt.plotly_sankey(k=5)

    print("Generating word clouds...")
    tt.word_clouds()

    print("Generating sentiment overlay...")
    tt.sentiment_overlay()

    print("files loaded:", lyrics_files)

if __name__ == '__main__':
    main()
