from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
import main_bot
import os
cod={'id':''}
RASTREAR,OPTION, CADASTRAR, LISTAR, DELETAR  = range(5)

def main() -> None:
   
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    src = os.getcwd()
    print(src)
    a = open("src","r")
    token = a.read()
    a.close()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_bot.start)],
        states={
            OPTION: [MessageHandler(Filters.regex('^(Rastrear)$'), main_bot.OpcRastreio),
                     MessageHandler(Filters.regex('^(Cadastrar)$'), main_bot.OpcCadastro),
                     MessageHandler(Filters.regex('^(Listar)$'), main_bot.OpcListar),
                     MessageHandler(Filters.regex('^(Deletar)$'), main_bot.OpcDeletar),
                     ],
            RASTREAR: [MessageHandler(Filters.text, main_bot.rastreiaEncomenda)],
            CADASTRAR: [MessageHandler(Filters.text, main_bot.cadastrarUsuario)],
            DELETAR: [MessageHandler(Filters.text, main_bot.deletaCodigo),]
        },
        fallbacks=[CommandHandler('cancel', main_bot.cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,main_bot.rastreiaEncomenda))
    dispatcher.add_handler(CommandHandler("start",main_bot.start))

        # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
