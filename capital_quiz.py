from __future__ import unicode_literals
import capitals_data as dataset
import random
from subprocess import Popen
from subprocess import PIPE
import sys


QUESTION_CAPITAL = "What is the capital of %s?\n\ta. %s\n\tb. %s\n\tc. %s\n"
QUESTION_COUNTRY = "%s is the capital of?\n\ta. %s\n\tb. %s\n\tc. %s\n"
DATA = dataset.data.items()

def makeQuestion(dataset, question_tuple, quiz_type):
  if quiz_type == 3:
    quiz_type = random.choice([1, 2])
  if quiz_type == 1:
    a, q = question_tuple
    options = random.sample([v[0] for v in dataset if v[0] != a], 2)
  else:
    q, a = question_tuple
    options = random.sample([v[1] for v in dataset if v[1] != a], 2)
  q = {"question": q, "answer": a, "options": options, "quiz_type": quiz_type}
  return q

def clearScreen():
  print chr(27) + "[2J"
  return

def confirmQuit():
  confirm = raw_input("Are you sure you want to quit? [Y|n]: ")
  if confirm in ("Y", "\r", "\n", ""):
    return True
  else:
    return False

def printScore(score, count, remaining):
  pct_complete = round(count/(count+remaining+0.)*100, 2)
  wrong = count - score
  if count > 0:
    pct_right = round((score/(count+0.))*100, 2)
  else:
    pct_right = 0.0
  sys.stdout.write(("\rFinal score after %s questions (%s%%): %s correct, "
                    "%s incorrect (%s%%).\n" % (count, pct_complete, score,
                                                wrong, pct_right)))
  sys.stdout.flush()

def runQuiz():
  score = 0
  count = 0
  data = DATA
  random.shuffle(data)
  quiz_type = int(raw_input("Quiz on Capitals (1), Countries (2) or Both (3): "))
  for i, capital_country in enumerate(data):
    q = makeQuestion(data, capital_country, quiz_type)
    opts = q["options"]
    opts.append(q["answer"])
    random.shuffle(opts)
    ans_index = opts.index(q["answer"])
    this_q = {"question": q["question"], "options": opts}
    if q["quiz_type"] == 1:
      output = QUESTION_CAPITAL % (this_q['question'], opts[0], opts[1], opts[2])
    else:
      output = QUESTION_COUNTRY % (this_q['question'], opts[0], opts[1], opts[2])
    resp = raw_input(output)
    if resp == "q":
      quit = confirmQuit()
      if quit:
        printScore(score, count, len(data) - i)
        return
      else:
        pass
    m = ["a", "b", "c"]
    clearScreen()
    if resp == m[ans_index]:
      score += 1
      count += 1
      sys.stdout.write("\rCorrect! Score: %s / %s (%s remaining)\n" %
                       (score,count, len(data) - 1 - i))
      sys.stdout.flush()
    else:
      count += 1
      sys.stdout.write("\rIncorrect. Score: %s / %s\n" % (score, count))
      sys.stdout.flush()
  printScore(score, count, remaining)


if __name__ == "__main__":
    runQuiz()