from __future__ import unicode_literals
import capitals_data as dataset
import random
from subprocess import Popen
from subprocess import PIPE
import sys


QUESTION = "What is the capital of %s?\n\ta. %s\n\tb. %s\n\tc. %s\n"


def makeQuestion(countries):
  a = random.choice(countries.keys())
  q = countries[a]
  options = random.sample([v for v in countries.keys() if v != a], 2)
  q = {"question": q, "answer": a, "options": options}
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
  data = dataset.data
  while data:
    q = makeQuestion(data)
    opts = q["options"]
    opts.append(q["answer"])
    random.shuffle(opts)
    ans_index = opts.index(q["answer"])
    this_q = {"question": q["question"], "options": opts}
    try:
      output = QUESTION % (this_q['question'], opts[0], opts[1], opts[2])
    except:
      print this_q
    resp = raw_input(output)
    if resp == "q":
      quit = confirmQuit()
      if quit:
        printScore(score, count, len(data))
        return
      else:
        pass
    m = ["a", "b", "c"]
    clearScreen()
    if resp == m[ans_index]:
      score += 1
      count += 1
      sys.stdout.write("\rCorrect! Score: %s / %s (%s remaining)\n" %
                       (score,count, len(data) - 1))
      sys.stdout.flush()
    else:
      count += 1
      sys.stdout.write("\rIncorrect. Score: %s / %s\n" % (score, count))
      sys.stdout.flush()
    data.pop(q["answer"])
  printScore(score, count, remaining)


if __name__ == "__main__":
    runQuiz()