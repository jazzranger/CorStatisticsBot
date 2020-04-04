import re
import telepot
from telepot.namedtuple import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import View
import json
from bot.utils import get_statistics, get_news
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string

# telepot.api.set_proxy('http://51.38.71.101:8080')


def _send_statistic(place):
    return render_to_string('stat.md', {'stat': get_statistics(place)})


def _send_help():
    return render_to_string('help.md')


def _send_news():
    return render_to_string('one_news.md', {'item': get_news()})


def _get_keyboard(func):
    if func != '/advices':
        reply_markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='/Russia')],
            [KeyboardButton(text='/All')],
            [KeyboardButton(text='/News')],
            [KeyboardButton(text='/Advices')],
        ], resize_keyboard=True)
    else:
        mylist = ['1. Мойте руки',
                  '2. Соблюдайте дистанцию']
        keyboard = [[InlineKeyboardButton(text=i, callback_data=f'/Advice{n}')] for n, i in enumerate(mylist, start=1)]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return reply_markup


def _send_advice(num):
    return render_to_string(f'advice{num}.md')


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print ('Callback Query:', query_id, from_id, query_data)


class CommandReceiver(View):
    def post(self, request, bot_token):

        commands = {
            '/news': _send_news(),
            '/start': _send_help(),
            '/help': _send_help(),
            '/russia': _send_statistic("Russia"),
            '/all': _send_statistic("All"),
            '/advices': 'Нажмите, чтобы увидеть подробную информацию:',
        }
        try:
            telegram_bot = telepot.Bot(bot_token)
            payload = json.loads(request.body.decode('utf-8'))
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text').lower()  # command
            keyboard = _get_keyboard(cmd)

            if re.match(r'/advice\d', cmd):
                result = _send_advice(cmd[-1])
            else:
                result = commands.get(cmd)

            if result:
                telegram_bot.sendMessage(chat_id, result, reply_markup=keyboard, parse_mode='Markdown')
            else:
                telegram_bot.sendMessage(chat_id, 'Я вас не понимаю, воспользуйтесь командой /help.')
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiver, self).dispatch(request, *args, **kwargs)
