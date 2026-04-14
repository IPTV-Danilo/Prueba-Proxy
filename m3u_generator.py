def generar_m3u(links):
    if not links:
        print("❌ No hay links para generar M3U")
        return

    contenido = "#EXTM3U\n"

    for i, link in enumerate(links, start=1):
        contenido += f'#EXTINF:-1 tvg-id="canal{i}" tvg-name="Canal {i}" group-title="TV",Canal {i}\n'
        contenido += f"{link}\n"

    with open("lista.m3u", "w") as f:
        f.write(contenido)

    print("✅ Lista M3U generada: lista.m3u")
