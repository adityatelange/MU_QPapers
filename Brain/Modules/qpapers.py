import re
import threading

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.chataction import ChatAction
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async

from Brain.Utils import button_menu, qpaper_utils
from Brain.Utils.dbfuncs import query_collect
from Brain.Utils.dbfuncs import user_collect, unavailable_collect
from Brain.Utils.strings import HELPER_SCRIPTS, COURSES_LIST, SEMS, BRANCHES_COURSE, BASE_URL
from Brain.Utils.user_info import get_user_info
from server import logger

qpapers_info_help = \
    """
        - /qpapers - Click to get Question Papers \U0001F4C3
    """
HELPER_SCRIPTS['qpapers'] = qpapers_info_help


@run_async
def qpapers_button(update, context):
    query = update.callback_query
    logger.info(query.data)
    course_match = re.match(r"qa=(.+?)", query.data)
    back_button_match = re.match(r"qa_back", query.data)
    try:
        if course_match:
            text = query.data.split('=', 1)[1].split('+')
            logger.info(text)

            back_data = "qa_back"
            button_list = []

            if len(text) == 1:
                # course selected => select branch
                colm = 2
                course = ""
                course_in = text[0]
                for module, tag in COURSES_LIST.items():
                    if course_in == tag:
                        course = module
                word = """Selected Course: `{}` \nSelect Branch :""".format(course)

                for branch, branch_code in BRANCHES_COURSE[course].items():
                    branch_full = branch
                    nextt = [course_in, branch_code]
                    button_list.append(
                        InlineKeyboardButton(
                            text="{}".format(branch_full),
                            callback_data="qa={}".format("+".join(nextt)), )
                    )

            elif len(text) == 2:
                # course, branch selected => select sem
                colm = 2
                course_full = branch_full = ''
                course_in, branch_in = text
                for module, tag in COURSES_LIST.items():
                    if course_in == tag:
                        course_full = module
                        break
                for branchy, key in BRANCHES_COURSE[course_full].items():
                    if branch_in == key:
                        branch_full = branchy
                        break
                word = """Selected Course: `{}` \nSelected Branch: `{}` \nSelect Sem :""". \
                    format(course_full, branch_full)

                for sem in range(1, SEMS[course_full] + 1):
                    nextt = [course_in, branch_in, str(sem)]
                    button_list.append(
                        InlineKeyboardButton(
                            text="{}".format(sem),
                            callback_data="qa={}".format("+".join(nextt)),
                        )
                    )

                # back_button data
                back_data = "qa={}".format("+".join([course_in]))

            elif len(text) == 3:
                # course, branch, sem selected => select subject
                colm = 1
                course_full = branch_full = ''
                course_in, branch_in, sem_in = text
                for module, tag in COURSES_LIST.items():
                    if course_in == tag:
                        course_full = module
                        break
                for branch, key in BRANCHES_COURSE[course_full].items():
                    if branch_in == key:
                        branch_full = branch
                        break

                word = """Selected Course: `{}` \nSelected Branch: `{}` \nSelected Sem: `{}` \nSelect Subject :""". \
                    format(course_full, branch_full, sem_in)

                # we don't use 'papers' here just use subs
                subs, papers = qpaper_utils.collect_subs_n_papers(course_full, branch_full, sem_in)

                pre = [course_in, branch_in, sem_in]
                if len(subs) == 0:
                    word += '\n _Unavailable_ \U0001F615'
                    query_log = {
                        'level': 3,
                        'course': course_full,
                        'branch': branch_full,
                        'semester': sem_in,
                        'subject': "",
                        'available': False
                    }
                    threading.Thread(target=unavailable_collect, args=(query_log,), daemon=True).start()
                else:
                    for sub in subs:
                        sub_ = ''.join(sub.split(' '))
                        callback_str = "qa={}".format('+'.join(pre))
                        callback_str += "+" + sub_

                        if len(callback_str) > 64:
                            logger.error("".join(text) + "=>" + callback_str + "#" + str(len(callback_str)))
                            callback_str = callback_str[:64]
                            logger.info("serialized to =>" + callback_str)

                        button_list.append(
                            InlineKeyboardButton(
                                text="{}".format(sub),
                                callback_data=callback_str,
                            )
                        )

                # back_button data
                back_data = "qa={}".format("+".join([course_in, branch_in]))

            elif len(text) == 4:
                # course, branch, sem, subject selected => send the links here
                colm = 1
                course_in, branch_in, sem_in, sub_in = text
                course_full = branch_full = ''

                for module, tag in COURSES_LIST.items():
                    if course_in == tag:
                        course_full = module
                        break
                for branch, key in BRANCHES_COURSE[course_full].items():
                    if branch_in == key:
                        branch_full = branch
                        break

                subs, papers = qpaper_utils.collect_subs_n_papers(course_full, branch_full, sem_in)
                is_avail = False
                if len(subs) == 0:
                    word = '\n _Unavailable_ \U0001F615'
                    query_log = {
                        'level': 4,
                        'course': course_full,
                        'branch': branch_full,
                        'semester': sem_in,
                        'subject': sub_in,
                        'available': False
                    }

                    threading.Thread(target=unavailable_collect, args=(query_log,), daemon=True).start()
                else:
                    sub_index = None
                    for sub in subs:
                        format_callback_sub = ''.join(sub.split(' '))[:53]
                        # print(repr(format_callback_sub) + " ================ " + repr(sub_in))

                        # https://stackoverflow.com/questions/17667923/remove-n-or-t-from-a-given-string

                        # removing \t \n \r when comparing
                        if re.sub('\s+', '', format_callback_sub) == re.sub('\s+', '', sub_in):
                            sub_index = subs.index(sub)
                            break

                    papers_for_sub = papers[sub_index].items()
                    for name, url in papers_for_sub:
                        button_list.append(
                            InlineKeyboardButton(
                                text="{}".format(name),
                                url=BASE_URL + url,
                            )
                        )

                    word = "Papers for \n`{}`".format(sub_in)
                    is_avail = True

                query_log = {
                    'level': 4,
                    'course': course_full,
                    'branch': branch_full,
                    'semester': sem_in,
                    'subject': sub_in,
                    'available': is_avail
                }
                threading.Thread(target=query_collect, args=(query_log,), daemon=True).start()

                # back_button data
                back_data = "qa={}".format("+".join([course_in, branch_in, sem_in]))
            else:
                colm = 1
                word = "Some Unknown Error\n Use /feedback to send feedback about this error)"

            # adding back button for easy traversing
            footer_button = [InlineKeyboardButton(text="[Back]", callback_data=back_data)]

            reply_markup_keyboard = InlineKeyboardMarkup(
                button_menu.build_menu(
                    button_list,
                    n_cols=colm,
                    footer_buttons=footer_button
                )
            )
            send_qpapers(update, text=word, keyboard=reply_markup_keyboard)

        elif back_button_match:
            get_qpapers(update, context)

        # ensure no spinning white circle
        context.bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as e:
        if e.message == "Message is not modified":
            pass
        elif e.message == "Query_id_invalid":
            pass
        elif e.message == "Message can't be deleted":
            pass
        else:
            logger.exception("Exception :  %s", str(query.data))


# do not async
def send_qpapers(update, text, keyboard=None):
    logger.info("into send_qpapers")
    if not keyboard:
        pass
    update.effective_message.reply_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


@run_async
def get_qpapers(update, context):
    logger.info("into get_qpapers")
    chat = update.effective_chat

    threading.Thread(target=user_collect, args=(get_user_info(update.effective_chat),), daemon=True).start()

    context.bot.send_chat_action(chat_id=chat.id, action=ChatAction.TYPING)
    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        send_qpapers(update, "Contact me in PM to get the list of possible commands.", InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Help",
                                   url="t.me/{}?start=help".format(
                                       context.bot.username))]]))
        return

    else:
        # called default
        button_list = []

        for module, tag in COURSES_LIST.items():
            callback_data = 'qa={}'.format(tag)
            text = "{}".format(module)
            button_list.append(
                InlineKeyboardButton(text=text,
                                     callback_data=callback_data, ))

        reply_markup_keyboard = InlineKeyboardMarkup(button_menu.build_menu(button_list, n_cols=2))

        send_qpapers(
            update=update,
            text="Select Course",
            keyboard=reply_markup_keyboard
        )
