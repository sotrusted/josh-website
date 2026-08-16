"""
Management command: python manage.py seed

Populates the database with content scraped from joshuashneider.com.
Safe to re-run — uses get_or_create throughout.
"""
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import SiteSettings
from pages.models import Page, Video, BandcampEmbed
from blog.models import Post

SCRAPED_DIR = settings.BASE_DIR / 'media' / 'uploads' / 'scraped'


def _copy_image(filename, dest_subdir):
    """Copy a scraped image into the media tree and return its relative path."""
    src = SCRAPED_DIR / filename
    if not src.exists():
        return None
    dest_dir = settings.MEDIA_ROOT / dest_subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / filename
    shutil.copy2(src, dest)
    return f'{dest_subdir}/{filename}'


class Command(BaseCommand):
    help = 'Seed the database with scraped content from joshuashneider.com'

    def handle(self, *args, **options):
        self.stdout.write('Seeding site settings…')
        self._seed_settings()

        self.stdout.write('Seeding flat pages…')
        self._seed_pages()

        self.stdout.write('Seeding videos…')
        self._seed_videos()

        self.stdout.write('Seeding blog posts…')
        self._seed_posts()

        self.stdout.write(self.style.SUCCESS('Done. Run: python manage.py createsuperuser'))

    # ------------------------------------------------------------------ #

    def _seed_settings(self):
        headshot = _copy_image('josh-headshot1.jpg', 'site')
        banner = _copy_image('cropped-cropped-sideways-angle.jpg', 'site')
        s = SiteSettings.get()
        s.site_name = 'Joshua Shneider'
        s.tagline = 'Composer · Saxophonist · Arranger'
        s.contact_email = 'contact@joshuashneider.com'
        s.bandcamp_url = 'https://joshuashneider.bandcamp.com'
        s.hero_text = (
            'Welcome to the website of Composer Joshua Shneider. '
            'Please take a look and a listen and let us know what you think — '
            "we'd love to hear from you!"
        )
        if headshot:
            s.hero_image = headshot
        if banner:
            s.header_banner = banner
        s.save()

    def _seed_pages(self):
        pages = [
            {
                'title': 'Bio',
                'slug': 'bio',
                'nav_order': 2,
                'content': BIO_CONTENT,
            },
            {
                'title': 'The Love Speaks Orchestra',
                'slug': 'orchestra',
                'nav_order': 3,
                'content': ORCHESTRA_CONTENT,
            },
            {
                'title': 'Services',
                'slug': 'services',
                'nav_order': 7,
                'content': SERVICES_CONTENT,
            },
            {
                'title': 'Lessons',
                'slug': 'lessons',
                'nav_order': 8,
                'content': LESSONS_CONTENT,
            },
            {
                'title': 'Sheet Music',
                'slug': 'sheet-music',
                'nav_order': 9,
                'content': SHEET_MUSIC_CONTENT,
            },
        ]
        for data in pages:
            page, created = Page.objects.get_or_create(slug=data['slug'])
            for k, v in data.items():
                setattr(page, k, v)
            page.save()
            status = 'created' if created else 'updated'
            self.stdout.write(f'  {status}: {data["title"]}')

        # Copy band poster for orchestra page
        img = _copy_image('Josh-Band-Poster-hi-res.jpg', 'pages')
        if img:
            orch = Page.objects.get(slug='orchestra')
            orch.hero_image = img
            orch.save()

    def _seed_videos(self):
        # Use full URLs so Josh sees the expected format in admin
        videos = [
            {
                'title': 'Lucy Woodward recording "When Love Speaks"',
                'youtube_url': 'https://www.youtube.com/watch?v=kxn5fuNy9PA',
                'description': (
                    'Lucy Woodward recording "When Love Speaks" by Josh and Finian McKean '
                    'with The Love Speaks Orchestra at Systems Two in Brooklyn, NY.'
                ),
                'order': 1,
            },
            {
                'title': '"Big Whup" from Systems Two session',
                'youtube_url': 'https://www.youtube.com/watch?v=rRV338FWpgo',
                'description': 'Featuring John O\'Gallagher on soprano saxophone.',
                'order': 2,
            },
            {
                'title': '"Gentle Soul"',
                'youtube_url': 'https://www.youtube.com/watch?v=ghzevciehEI',
                'description': (
                    'Featuring Dan Pratt on tenor saxophone. '
                    'A mashup of two well-known songs from different eras — '
                    'let us know if you can name them both…'
                ),
                'order': 3,
            },
            {
                'title': '"Cooler Heads" (live)',
                'youtube_url': 'https://www.youtube.com/watch?v=Qrevu2Sv8dA',
                'description': (
                    'Featuring Daniel Dickinson on alto saxophone and Andrew Gravish on trumpet.'
                ),
                'order': 4,
            },
            {
                'title': '"Lost In The Stars" — Saundra Williams',
                'youtube_url': 'https://www.youtube.com/watch?v=hK9d12zUSvM',
                'description': (
                    'The inimitable Saundra Williams singing Josh\'s arrangement of '
                    'Kurt Weill and Maxwell Anderson\'s "Lost In The Stars".'
                ),
                'order': 5,
            },
        ]
        for data in videos:
            vid, created = Video.objects.get_or_create(youtube_url=data['youtube_url'])
            for k, v in data.items():
                setattr(vid, k, v)
            vid.save()
            status = 'created' if created else 'updated'
            self.stdout.write(f'  {status}: {data["title"]}')

    def _seed_posts(self):
        posts = [
            {
                'title': 'The Love Speaks Orchestra debuts at #8 on the Roots Music Report',
                'slug': 'love-speaks-orchestra-roots-music-report',
                'category': 'news',
                'content': NEWS_ROOTS_MUSIC,
                'image_filename': 'Roots-Music-3.7.14-jpg.jpg',
            },
            {
                'title': 'WBGO New York\'s Jazz Station is spinning The Love Speaks Orchestra',
                'slug': 'wbgo-love-speaks-orchestra',
                'category': 'news',
                'content': NEWS_WBGO,
                'image_filename': 'WBGO-logo-jpg.jpg',
            },
            {
                'title': 'Debut CD on Brooklyn Jazz Underground Records',
                'slug': 'debut-cd-brooklyn-jazz-underground',
                'category': 'news',
                'content': NEWS_BJU,
                'image_filename': 'Josh_cvr_hi-300x266.jpg',
            },
            {
                'title': 'The Love Speaks Orchestra at Slope Lounge — October 1, 2018',
                'slug': 'love-speaks-orchestra-slope-lounge-2018',
                'category': 'events',
                'content': EVENT_SLOPE_LOUNGE,
                'image_filename': 'Josh-Band-Poster-hi-res.jpg',
            },
            {
                'title': 'ShapeShifter Lab — November 2013',
                'slug': 'shapeshifter-lab-november-2013',
                'category': 'events',
                'content': EVENT_SHAPESHIFTER,
                'image_filename': '1396996_765995053241_1738550416_o_2-300x141.jpg',
            },
            {
                'title': 'NYC Composers Now Festival — February 2014',
                'slug': 'composers-now-festival-2014',
                'category': 'events',
                'content': EVENT_COMPOSERS_NOW,
                'image_filename': 'Composers-Now-Blue-Logo-300x100.jpg',
            },
        ]

        for data in posts:
            image_filename = data.pop('image_filename', None)
            post, created = Post.objects.get_or_create(slug=data['slug'])
            for k, v in data.items():
                setattr(post, k, v)

            if image_filename:
                img = _copy_image(image_filename, 'blog')
                if img:
                    post.image = img
            post.save()
            status = 'created' if created else 'updated'
            self.stdout.write(f'  {status}: {data["title"]}')


# ------------------------------------------------------------------ #
# Content strings
# ------------------------------------------------------------------ #

BIO_CONTENT = """
<p>Composer and Saxophonist Joshua Shneider has enjoyed a career that has included writing for
and playing with some of the most inspiring and inspired artists of our time. He has had his
compositions and arrangements performed and/or recorded by Donald Brown, James Williams, Bill Pierce,
John Abercrombie, George Bohanon, Howard Johnson, John McNeil, Mark Feldman, Christian Howes,
Lucy Woodward, The Bill Mobley Jazz Orchestra, The BMI Jazz Orchestra and many others.</p>

<p>He is the leader of The Joshua Shneider Love Speaks Orchestra, a 19 piece ensemble performing
his original compositions and arrangements. He has collaborated on music for the theater with
playwrights Eve Ensler and Rosemary Moore. He is a founding member of Pulse, a chamber ensemble
of composers and performers dedicated to presenting contemporary music without boundaries.</p>

<p>Joshua Shneider began his career as a saxophonist playing with a variety of artists from across
the musical spectrum, such as Felix Cavaliere, John Sebastian, Geoff Muldaur, Tom Rush, Robbie Dupree,
John Hall, esteemed Jazz Educator Clem De Rosa, Matt Guitar Murphy and The Mighty Sparrow among others.
His saxophone has also been featured with an array of Theater and Film artists, which include director
Lee Breuer and composer Bob Telson (<em>The Gospel at Colonus, The Warrior Ant,</em> and the recording
<em>"Calling You"</em>), and filmmaker Percy Adlon (<em>Bagdad Cafe, Hawaiian Gardens</em>).</p>

<p>He has been quoted extensively in the book <em>"Thinking in Jazz: The Infinite Art of Improvisation"</em>
by Paul F. Berliner, pub. 1994, Univ. of Chicago Press.</p>

<p>Joshua Shneider has been recognized by The National Endowment for the Arts, Meet the Composer,
ASCAP, The International Association of Jazz Education, the BMI Jazz Composers Workshop and the
Brooklyn Arts Council. He was named a 2012 recipient of an American Music Center CAP Recording Grant
for new music by American Composers made possible by endowment funds from the Mary Flagler Cary
Charitable Trust.</p>

<p>Joshua Shneider received his BM and MM in Composition from the Manhattan School of Music where
he studied with Ludmila Ulehla, Manny Albam, David Berger, Richard De Rosa and Giampalo Bracali.
As a saxophonist he has studied with Joe Viola, George Coleman, Eddie Daniels and Barry Harris.</p>

<p>Joshua Shneider lives in Brooklyn, New York, with his wife, playwright Rosemary Moore.</p>
"""

ORCHESTRA_CONTENT = """
<p>The Joshua Shneider Love Speaks Orchestra is a 19 piece ensemble comprised of some of NYC's
most illustrious and adventurous improvisers, interpreting the music and arrangements of Joshua Shneider.</p>

<p>Melodic, grooving, searching and harmonically inventive, the music draws inspiration from a wide
variety of musical influences and includes Jazz, R&amp;B, World and American Pop elements.</p>

<p>Pop/Soul singing sensations Lucy Woodward and Saundra Williams grace the stage as special guests
with the Love Speaks Orchestra.</p>

<p>Check us out on the <a href="/listen/">Listen</a> page! For bookings please <a href="/contact/">get in touch</a>.</p>
"""

SERVICES_CONTENT = """
<p>Joshua Shneider is available to provide an assortment of music services:</p>

<ul>
<li><strong>Music Production</strong> — for recordings, film or live performance</li>
<li><strong>Commission</strong> — an original piece or an arrangement for your ensemble</li>
<li><strong>Artist Residency / Teaching Artist Workshops</strong></li>
<li><strong>Private Teaching</strong></li>
<li><strong>Score Catalog</strong> — purchase charts by Joshua Shneider for your ensemble</li>
<li><strong>Score Preparation, Transposition and Transcription</strong></li>
</ul>

<p><a href="/contact/">Contact us here</a> to discuss your project.</p>
"""

LESSONS_CONTENT = """
<p>Joshua Shneider offers private lessons in the following:</p>

<h3>Composition, Arranging &amp; Music Theory</h3>
<p>Lessons include score study, music notation and transcription.</p>

<h3>Saxophone, Clarinet &amp; Flute</h3>
<p>Learn technique, sight reading, improvisation and ear training.</p>

<p>Joshua has a Masters Degree from the Manhattan School of Music and is an experienced teacher
(NYC Dept of Education through College). He has many recording credits as a Saxophonist, Composer
and Arranger. Lessons are tailored to individual interests and can be geared toward a specific project.</p>

<p>Convenient Brooklyn, New York studio, or online. Returning students encouraged.</p>

<blockquote>
<p>"I have been a working musician my entire adult life. I am drawn to the contrast between the
unfathomable mystery and the logical earthiness of music. To be a musician is to be a listener;
as such, I am constantly inspired by my students. I'm immensely gratified by their progress,
and I hope to share with them the love of music that continues to reward and challenge me."</p>
</blockquote>

<p><a href="/contact/">Contact us</a> for more information.</p>
"""

SHEET_MUSIC_CONTENT = """
<p>Download free study scores or purchase full score and parts from our catalog.</p>
<p>More scores coming soon! If you don't see what you want, please <a href="/contact/">get in touch</a>.</p>

<ul>
<li>Dark Energy <em>(score)</em></li>
<li>Friction <em>(score)</em></li>
<li>Lover's Leap <em>(score)</em></li>
</ul>

<p>Full score and parts available on request. Contact us for pricing and ordering.</p>
"""

NEWS_ROOTS_MUSIC = """
<p>The Love Speaks Orchestra debuts at <strong>#8 on the "Roots Music Report's Weekly Top 50 Jazz Album Chart"</strong>!</p>

<p>The new Love Speaks Orchestra CD has been getting great exposure in print, online, and on the radio,
nationally and around the world. We've been featured in the U.K., Belgium, The Netherlands, Italy,
Canada, Japan and Brazil.</p>

<p>We're adding new radio stations every week in the U.S. with significant airplay in cities such as
Chicago, Philadelphia, Minneapolis, Miami, Los Angeles, San Francisco, San Diego, Honolulu, New Orleans,
Las Vegas, Cleveland, Dallas and many others. Many thanks especially to all the NPR and College Radio
affiliates for the wonderful support, as well as to the many internet stations spreading the word!</p>
"""

NEWS_WBGO = """
<p>WBGO, New York's Jazz Station is spinning The Love Speaks Orchestra!</p>

<p>We're thrilled to be getting played on our hometown station. Many thanks to Gary Walker and the
staff for bringing our music to the pungent NYC airwaves! Between Mancini and Miles… pretty groovy.</p>
"""

NEWS_BJU = """
<p>We're pleased to announce that the debut CD of the Love Speaks Orchestra has been released on
<strong>Brooklyn Jazz Underground Records</strong>! BJU Records is an amazing label committed to
creative and adventurous contemporary improvised music. We are thrilled to be associated with the
label and their artists. Please check out their website at
<a href="http://www.bjurecords.com" target="_blank" rel="noopener">bjurecords.com</a>.</p>

<p>The CD was recorded at the wonderful Systems Two recording studio in Brooklyn, New York and was
co-produced by "the Jedi Master" Jeff Jones, and mixed by Lincoln Schleifer. The band sounds amazing,
and we were joined by special guests Dave Stryker on guitar (ferocious), and the indomitable
Lucy Woodward on vocals.</p>

<p>This project is supported by the American Music Center's CAP Recording Program, made possible
by endowment funds from the Mary Flagler Cary Charitable Trust.</p>
"""

EVENT_SLOPE_LOUNGE = """
<p>The Love Speaks Orchestra is coming to the brand new <strong>Slope Lounge</strong> in Park Slope,
Brooklyn as part of the continuing Monday Night LIVING LARGE Ensemble Series!</p>

<p><strong>Monday, October 1st, 2018 at 8pm</strong><br>
837 Union Street, Brooklyn, New York 11215</p>
"""

EVENT_SHAPESHIFTER = """
<p>The Love Speaks Orchestra at <strong>ShapeShifter Lab</strong>, November 2013.</p>

<p>Tuesday, November 19th, 2013 · 8pm · $10 · All ages<br>
18 Whitwell Place, Brooklyn, NY 11215<br>
(Between 1st and Carroll St, off 4th Ave — Park Slope)<br>
+1-646-820-9452</p>

<p>We were also video streaming live at
<a href="http://live.shapeshifterlab.com" target="_blank" rel="noopener">live.shapeshifterlab.com</a></p>
"""

EVENT_COMPOSERS_NOW = """
<p>The Love Speaks Orchestra returns to the <strong>"Size Matters" Large Ensemble series</strong>
in Park Slope, Brooklyn.</p>

<p><strong>February 24, 2014 at 8pm</strong><br>
The Tea Lounge, 837 Union St, Brooklyn, NY 11215</p>

<p>As part of the <strong>February 2014 NYC Composers Now Festival</strong>,
Sponsored by The Fund For The City of New York.</p>

<p>Come celebrate our debut Brooklyn Jazz Underground Records release! Featuring:<br>
John O'Gallagher, Matthew Willis, Dan Pratt, Quinsin Nachoff, Frank Basile — woodwinds<br>
Matthew McDonald, Noah Bless, John Yao, Max Seigel — trombones<br>
Jeff Wilfore, Alexander Pope Norris, David Smith, Andy Gravish — trumpets<br>
Eric Halvorson — drums · Evan Gregor — bass · Bennett Paster — keys · Joe Cardello — percussion</p>

<p>Special Guests: vocalist Saundra Williams (lately of Sharon Jones and the Dap Kings)
and guitar hero Dave Stryker.</p>
"""
