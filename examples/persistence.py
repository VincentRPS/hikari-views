import hikari
import miru

# If you want your components to work and persist after an application restart,
# you have to make them persistent. There are two conditions to this:
# - The view's timeout must explicitly be set to None
# - All components MUST have a unique custom_id
# It is recommended to tie custom_ids to some variable to ensure they do not match,
# to avoid conflicts. (e.g. a UUID stored in a database), but that is outside the
# scope of this example.

# Tip: It is recommended to subclass components to have the ability to pass
# custom_id variables. See the subclassed example on how to do this.

# Tip 2: To check if your view can be persistent or not, use the View.is_persistent
# boolean property.


class Persistence(miru.View):
    def __init__(self, app: hikari.GatewayBot) -> None:
        super().__init__(app, timeout=None)  # Setting timeout to None

    @miru.button(label="Button 1", custom_id="my_unique_custom_id_1")
    async def button_one(self, button: miru.Button, interaction: miru.Interaction) -> None:
        await interaction.send_message("You pressed button 1.")

    @miru.button(label="Button 2", custom_id="my_unique_custom_id_2")
    async def button_two(self, button: miru.Button, interaction: miru.Interaction) -> None:
        await interaction.send_message("You pressed button 2.")


bot = hikari.GatewayBot("...")


@bot.listen()
async def startup_views(event: hikari.StartedEvent) -> None:
    # You must reinstantiate the view in the same state it was before shutdown (e.g. same custom_ids)
    view = Persistence(bot)
    # Restart the listener for the view, you may optionally pass in a message_id to further improve
    # accuracy and avoid conflicts from matching custom_ids.
    view.start_listener()


@bot.listen()
async def buttons(event: hikari.GuildMessageCreateEvent) -> None:

    # Do not process messages from bots or empty messages
    if event.is_bot or not event.content:
        return

    if event.content.startswith("miru"):
        view = Persistence(bot)
        message = await event.message.respond(
            "This is a persistent component menu, and works after bot restarts!", components=view.build()
        )

        view.start(message)


bot.run()
