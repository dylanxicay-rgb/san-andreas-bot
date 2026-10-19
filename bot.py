import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"¡Conectado con éxito como {bot.user}!")
  try:
    synced = await bot.tree.sync()
    print(f"Se sincronizaron {len(synced)} comandos correctamente.")
  except Exception as e:
    print(e)


@bot.tree.command(
    name="vehiculo",
    description=(
        "Publica una ficha detallada de auto en el foro de S.A. Dealership"
    ),
)
@app_commands.describe(
    vehiculo="Nombre del vehículo (Ej: Pfister Comet)",
    millas="Millas / Recorrido (Ej: 12,400 mi)",
    precio="Precio de venta (Ej: $185,000)",
    bloqueo="Nivel de Bloqueo (Ej: Nivel 3)",
    alarma="Nivel de Alarma (Ej: Nivel 2)",
    antirrobo="Nivel de Antirrobo (Ej: Nivel 1)",
    motor="Nivel de Motor (Ej: Nivel 4)",
    frenos="Nivel de Frenos (Ej: Nivel 2)",
    suspension="Nivel de Suspensión (Ej: Nivel 3)",
    transmision="Nivel de Transmisión (Ej: Nivel 3)",
    extras="Extras instalados (Ej: Turbo, Llantas custom, Blindaje)",
    imagen="Sube, arrastra o pega tu foto aquí",
)
async def vehiculo(
    interaction: discord.Interaction,
    vehiculo: str,
    millas: str,
    precio: str,
    bloqueo: str,
    alarma: str,
    antirrobo: str,
    motor: str,
    frenos: str,
    suspension: str,
    transmision: str,
    extras: str,
    imagen: discord.Attachment,
):
  await interaction.response.defer(ephemeral=True)

  # -------------------------------------------------------------
  # 👇 TU ID DE CANAL TIPO FORO 👇
  # -------------------------------------------------------------
  ID_CANAL_CATALOGO = 1556110821468282890  # <--- Mantén aquí tu ID de foro

  try:
    canal_destino = bot.get_channel(
        ID_CANAL_CATALOGO
    ) or await bot.fetch_channel(ID_CANAL_CATALOGO)

    if canal_destino:
      color_bronce = discord.Color.from_rgb(212, 175, 55)

      embed = discord.Embed(
          title="✨ S.A. DEALERSHIP • EXCLUSIVE SHOWROOM ✨",
          description=(
              f"🏎️ **Vehículo:** **{vehiculo}**\n*Disponible para entrega"
              f" inmediata.*\n\n💎 **Precio:** **{precio}**"
          ),
          color=color_bronce,
      )

      # Millas corregido en una sola línea
      embed.add_field(
          name="📊 Millas / Recorrido", value=f"Millas: {millas}", inline=False
      )

      # Apartado de Seguridad (sin barras extra)
      texto_seguridad = (
          f" **Bloqueo:** {bloqueo}\n"
          f" **Alarma:** {alarma}\n"
          f" **Antirrobo:** {antirrobo}"
      )
      embed.add_field(
          name="🛡️ Apartado de Seguridad", value=texto_seguridad, inline=False
      )

      # Apartado de Mecánica
      texto_mecanica = (
          f" **Motor:** {motor}\n"
          f" **Frenos:** {frenos}\n"
          f" **Suspensión:** {suspension}\n"
          f" **Transmisión:** {transmision}"
      )
      embed.add_field(
          name="🔧 Apartado de Mecánica", value=texto_mecanica, inline=False
      )

      # Extras
      embed.add_field(name="➕ Extras", value=extras, inline=False)

      embed.set_image(url=imagen.url)
      embed.set_footer(
          text="S.A. Dealership • Calidad y Confianza Garantizada 🌟"
      )

      if isinstance(canal_destino, discord.ForumChannel):
        await canal_destino.create_thread(name=vehiculo, embed=embed)
      else:
        await canal_destino.send(embed=embed)

      await interaction.followup.send(
          "¡Vehículo publicado en el foro con éxito!", ephemeral=True
      )
    else:
      await interaction.followup.send(
          "❌ Error: El bot no encuentra el canal. Revisa el ID.",
          ephemeral=True,
      )

  except Exception as error_envio:
    print(f"Error al publicar en el foro: {error_envio}")
    await interaction.followup.send(
        f"❌ Error al publicar: El bot necesita permisos para crear publicaciones"
        f" en ese foro. ({error_envio})",
        ephemeral=True,
    )


# TU TOKEN:
os.getenv("DISCORD_TOKEN")