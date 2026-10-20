import os
import threading
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask

# --- CONFIGURACIÓN DE FLASK PARA EL PUERTO DE RENDER ---
app = Flask(__name__)

@app.route("/")
def home():
    return "¡El bot de San Andreas Dealership esta activo 24/7!"

# --- CONFIGURACIÓN DEL BOT DE DISCORD ---
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Conectado con exito como {bot.user}")
    try:
        id_servidor = discord.Object(id=1556110821468282890)
        
        # Limpia y sincroniza el comando de manera limpia en el servidor
        bot.tree.clear_commands(guild=id_servidor)
        synced = await bot.tree.sync(guild=id_servidor)
        
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error al sincronizar: {e}")

@bot.tree.command(
    name="auto",
    description="Publica una ficha detallada de auto en el foro de S.A. Dealership",
)
@app_commands.describe(
    vehiculo="Nombre del vehiculo (Ej: Pfister Comet)",
    millas="Millas / Recorrido (Ej: 12,400 mi)",
    precio="Precio de venta (Ej: $185,000)",
    bloqueo="Nivel de Bloqueo (Ej: Nivel 3)",
    alarma="Nivel de Alarma (Ej: Nivel 2)",
    antirrobo="Nivel de Antirrobo (Ej: Nivel 1)",
    motor="Nivel de Motor (Ej: Nivel 4)",
    frenos="Nivel de Frenos (Ej: Nivel 2)",
    suspension="Nivel de Suspension (Ej: Nivel 3)",
    transmision="Nivel de Transmision (Ej: Nivel 3)",
    extras="Extras instalados (Ej: Turbo, Llantas custom, Blindaje)",
    imagen="Sube, arrastra o pega tu foto aqui",
)
async def auto(
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
    ID_CANAL_CATALOGO = 1556110821468282890

    try:
        canal_destino = bot.get_channel(ID_CANAL_CATALOGO) or await bot.fetch_channel(ID_CANAL_CATALOGO)
        if canal_destino:
            color_bronce = discord.Color.from_rgb(212, 175, 55)
            embed = discord.Embed(
                title="S.A. DEALERSHIP • EXCLUSIVE SHOWROOM",
                description=f"Vehiculo: **{vehiculo}**\n*Disponible para entrega inmediata.*\n\nPrecio: **{precio}**",
                color=color_bronce,
            )
            embed.add_field(name="Millas / Recorrido", value=f"Millas: {millas}", inline=False)
            
            texto_seguridad = f"Bloqueo: {bloqueo}\nAlarma: {alarma}\nAntirrobo: {antirrobo}"
            embed.add_field(name="Apartado de Seguridad", value=texto_seguridad, inline=False)
            
            texto_mecanica = f"Motor: {motor}\nFrenos: {frenos}\nSuspension: {suspension}\nTransmision: {transmision}"
            embed.add_field(name="Apartado de Mecanica", value=texto_mecanica, inline=False)
            
            embed.add_field(name="Extras", value=extras, inline=False)
            embed.set_image(url=imagen.url)
            embed.set_footer(text="S.A. Dealership • Calidad y Confianza Garantizada")

            if isinstance(canal_destino, discord.ForumChannel):
                await canal_destino.create_thread(name=vehiculo, embed=embed)
            else:
                await canal_destino.send(embed=embed)

            await interaction.followup.send("¡Vehiculo publicado en el foro con exito!", ephemeral=True)
        else:
            await interaction.followup.send("Error: El bot no encuentra el canal.", ephemeral=True)
    except Exception as error_envio:
        print(f"Error al publicar en el foro: {error_envio}")
        await interaction.followup.send(f"Error al publicar: ({error_envio})", ephemeral=True)

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    threading.Thread(target=lambda: bot.run(os.getenv("DISCORD_TOKEN")), daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
