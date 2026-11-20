# Undangan Tedhak Siten Giaksa & Giakta

Static invitation website, hosted on Vercel. Every push to `main` redeploys automatically.

## Add photos to the gallery

1. Open the `public/gallery` folder on GitHub.
2. Click **Add file → Upload files**, drop the photos in, and click **Commit changes**.
3. Vercel redeploys within about a minute and the new photos appear in "Our Gallery".

Photos are sorted by file name (`01.jpg`, `02.jpg`, `10.jpg` ...), so name them with numbers to control the order.
Supported: `.jpg`, `.jpeg`, `.png`, `.webp`. Keep each file under ~1 MB for fast loading (resize to about 1600 px on the long side).
To remove a photo, delete the file from `public/gallery`.

## Personalised guest link

Add `?to=Nama+Tamu` to the link, e.g. `https://<domain>/?to=Keluarga+Besar+Astra`.
The cover will show "Kepada Yth. Keluarga Besar Astra".

## Background music (optional)

Upload an MP3 named `music.mp3` into `public/`. A music button appears automatically and the song starts when the guest taps "Buka Undangan".

## Other photos

| Section | File |
| --- | --- |
| Cover / top | `public/assets/img/cover.jpg` |
| Tedhak Siten text (with parents) | `public/assets/img/orang-tua.jpg` |
| Close up Giaksa | `public/assets/img/giaksa.jpg` |
| Close up Giakta | `public/assets/img/giakta.jpg` |
| Closing | `public/assets/img/penutup.jpg` |

Replace a file with one of the same name to swap the photo.

## Wishes & RSVP

Not included yet because it needs a database. Options for later: Supabase table + small API route, or a Google Form embedded in a new section.
