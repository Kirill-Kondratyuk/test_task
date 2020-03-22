from threading import Thread

from parser import Sender
from models import session, Task


with open('dict.txt', 'r') as f:
    wordlist = f.read()

wordlist = wordlist.split('\n')
last_word = wordlist[0]

has_rows = session.query(Task).first()

if has_rows:
    task = session.query(Task).order_by(Task.id.desc()).first()
    if task.completed:
        print('[!] Last task was completed. Creating the new one...')
        task = Task(completed=False, last_word='')
        session.add(task)
        session.commit()
        task_id = task.id
    else:
        task_id = task.id
        last_word = task.last_word
        if not last_word:
            last_word = wordlist[0]
        print('[!] Last task wasn"t completed. Resuming from <{}> word'.format(last_word))

else:
    print('[!] Task table is empty. Creating the new one...')
    task = Task(completed=False, last_word='')
    session.add(task)
    session.commit()
    task_id = task.id


if last_word != wordlist[0]:
    index = wordlist.index(last_word)
    wordlist = wordlist[index:]

sublist_length = len(wordlist)//60

if sublist_length < 1:
    graber = Sender(words_list=wordlist, task_id=task_id)
    graber.process_list()
    task = session.query(Task).order_by(Task.id.desc()).first()
    task.completed = 1
    session.commit()
    print('[!} Search finished!')
else:
    lists = [wordlist[x:x+sublist_length] for x in range(0, len(wordlist), sublist_length)]

    def do_work(key_words):
        _graber = Sender(words_list=key_words, task_id=task_id)
        _graber.process_list()

    for i in range(0, 10, 1):
        x = Thread(target=do_work, args=(lists[i],))
        x.start()
        x.join()
    print('[!] Search finished!')
    task.completed = 1
    session.commit()
