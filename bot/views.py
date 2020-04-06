import telepot
from telepot.namedtuple import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import View
import json
from bot.utils import get_statistics, get_news, get_statistics_history
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string

telepot.api.set_proxy('http://51.38.71.101:8080')


def _send_statistic(place):
    return render_to_string('stat.md', {'stat': get_statistics(place)})


def _send_help():
    return render_to_string('help.md')


def _send_news():
    return render_to_string('one_news.md', {'item': get_news()})


def _send_advices():
    return render_to_string(f'advices.md')


class CommandReceiver(View):
    def post(self, request, bot_token):

        commands = {
            '/start': _send_help(),
            'news': _send_news(),
            'help': _send_help(),
            'russia': _send_statistic("Russia"),
            'all': _send_statistic("All"),
            'advices': _send_advices(),
        }
        reply_markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Russia')],
            [KeyboardButton(text='All')],
            [KeyboardButton(text='News')],
            [KeyboardButton(text='Advices')],
        ], resize_keyboard=True)
        try:
            telegram_bot = telepot.Bot(bot_token)
            payload = json.loads(request.body.decode('utf-8'))
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text').lower()
            result = commands.get(cmd)
            if result:
                telegram_bot.sendMessage(chat_id, result, reply_markup=reply_markup, parse_mode='Markdown')
                print(cmd)
                if cmd == 'all' or cmd == 'russia':
                    telegram_bot.sendPhoto(chat_id, get_statistics_history(cmd))
            else:
                telegram_bot.sendMessage(chat_id, 'Я вас не понимаю, воспользуйтесь командой /help.')
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiver, self).dispatch(request, *args, **kwargs)
