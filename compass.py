#!/usr/bin/env python3

import urllib
import urllib.request
import lxml.html
import matplotlib.pyplot as pyplot

url = "http://www.politicalcompass.org/test"
def_opts = {"pageno": 1, "carried_x": 0, "carried_y": 0, "submit": "Next Page"}
def_answers = {
	1: 3,	2: 0,	3: 3,	4: 0,	5: 0,	6: 0,	7: 0,

	8: 2,	9: 2,	10: 3,	11: 2,	12: 0,	13: 1,	14: 1,	15: 0,	16: 2,
	17: 1,	18: 2,	19: 3,	20: 2,	21: 2,

	22: 0,	23: 3,	24: 0,	25: 0,	26: 0,	27: 0,	28: 0,	29: 3,	30: 3,
	31: 0,	32: 1,	33: 0,	34: 1,	35: 1,	36: 0,	37: 0,	38: 0,	39: 0,

	40: 3,	41: 0,	42: 0,	43: 0,	44: 0,	45: 0,	46: 0,	47: 0,	48: 0,
	49: 0,	50: 1,	51: 0,

	52: 0,	53: 0,	54: 1,	55: 0,	56: 0,

	57: 0,	58: 3,	59: 3,	60: 3,	61: 0,	62: 0
}
values = {0: "Strongly Disagree", 1: "Disagree", 2: "Agree", 3: "Strongly Agree"}

def_questions = {
	1:	"If economic globalisation is inevitable, it should primarily serve humanity rather than the interests of trans-national corporations.",
	2:	"I'd always support my country, whether it was right or wrong.",
	3:	"No one chooses his or her country of birth, so it's foolish to be proud of it.",
	4:	"Our race has many superior qualities, compared with other races.",
	5:	"The enemy of my enemy is my friend.",
	6:	"Military action that defies international law is sometimes justified.",
	7:	"There is now a worrying fusion of information and entertainment.",
	8:	"People are ultimately divided more by class than by nationality.",
	9:	"Controlling inflation is more important than controlling unemployment.",
	10:	"Because corporations cannot be trusted to voluntarily protect the environment, they require regulation.",
	11:	"\"from each according to his ability, to each according to his need\" is a fundamentally good idea.",
	12:	"It's a sad reflection on our society that something as basic as drinking water is now a bottled, branded consumer product.",
	13:	"Land shouldn't be a commodity to be bought and sold.",
	14:	"It is regrettable that many personal fortunes are made by people who simply manipulate money and contribute nothing to their society.",
	15:	"Protectionism is sometimes necessary in trade.",
	16:	"The only social responsibility of a company should be to deliver a profit to its shareholders.",
	17:	"The rich are too highly taxed.",
	18:	"Those with the ability to pay should have the right to higher standards of medical care .",
	19:	"Governments should penalise businesses that mislead the public.",
	20:	"A genuine free market requires restrictions on the ability of predator multinationals to create monopolies.",
	21:	"The freer the market, the freer the people.",
	22:	"Abortion, when the woman's life is not threatened, should always be illegal.",
	23:	"All authority should be questioned.",
	24:	"An eye for an eye and a tooth for a tooth.",
	25:	"Taxpayers should not be expected to prop up any theatres or museums that cannot survive on a commercial basis.",
	26:	"Schools should not make classroom attendance compulsory.",
	27:	"All people have their rights, but it is better for all of us that different sorts of people should keep to their own kind.",
	28:	"Good parents sometimes have to spank their children.",
	29:	"It's natural for children to keep some secrets from their parents.",
	30:	"Possessing marijuana for personal use should not be a criminal offence.",
	31:	"The prime function of schooling should be to equip the future generation to find jobs.",
	32:	"People with serious inheritable disabilities should not be allowed to reproduce.",
	33:	"The most important thing for children to learn is to accept discipline.",
	34:	"There are no savage and civilised peoples; there are only different cultures.",
	35:	"Those who are able to work, and refuse the opportunity, should not expect society's support.",
	36:	"When you are troubled, it's better not to think about it, but to keep busy with more cheerful things.",
	37:	"First-generation immigrants can never be fully integrated within their new country.",
	38:	"What's good for the most successful corporations is always, ultimately, good for all of us.",
	39:	"No broadcasting institution, however independent its content, should receive public funding.",
	40:	"Our civil liberties are being excessively curbed in the name of counter-terrorism.",
	41:	"A significant advantage of a one-party state is that it avoids all the arguments that delay progress in a democratic political system.",
	42:	"Although the electronic age makes official surveillance easier, only wrongdoers need to be worried.",
	43:	"The death penalty should be an option for the most serious crimes.",
	44:	"In a civilised society, one must always have people above to be obeyed and people below to be commanded.",
	45:	"Abstract art that doesn't represent anything shouldn't be considered art at all.",
	46:	"In criminal justice, punishment should be more important than rehabilitation.",
	47:	"It is a waste of time to try to rehabilitate some criminals.",
	48:	"The businessperson and the manufacturer are more important than the writer and the artist.",
	49:	"Mothers may have careers, but their first duty is to be homemakers.",
	50:	"Multinational companies are unethically exploiting the plant genetic resources of developing countries.",
	51:	"Making peace with the establishment is an important aspect of maturity.",
	52:	"Astrology accurately explains many things.",
	53:	"You cannot be moral without being religious.",
	54:	"Charity is better than social security as a means of helping the genuinely disadvantaged.",
	55:	"Some people are naturally unlucky.",
	56:	"It is important that my child's school instills religious values.",
	57:	"Sex outside marriage is usually immoral.",
	58:	"A same sex couple in a stable, loving relationship, should not be excluded from the possibility of child adoption.",
	59:	"Pornography, depicting consenting adults, should be legal for the adult population.",
	60:	"What goes on in a private bedroom between consenting adults is no business of the state.",
	61:	"No one can feel naturally homosexual.",
	62:	"These days openness about sex has gone too far."
}


def submit_page(post_args=None):
	'''
	Returns response body, as UTF8-decoded <str>
	'''

	req = urllib.request.Request(url)

	if isinstance(post_args, dict) and "submit" in post_args:
		post = urllib.parse.urlencode(post_args)
		# print(post_args)
		# print(post.encode('ascii'))
		req.add_data(post.encode('ascii'))

	response = urllib.request.urlopen(req)
	data = response.readall()
	return(data.decode())


def reap_questions(html):
	questions = {}
	for tag in html.findall(".//label[1]/input[@type='radio']"):
		num = int(tag.name.split('_')[-1])
		questions[num] = tag.find("....../td[1]").text_content()
	return questions


def compass():
	answers = def_answers.copy()
	questions = {}
	post_args = {}

	while post_args is not None:
		# Post previous responses, Get new questions (first post is empty, gets page 1)
		html_text = submit_page(post_args)
		html = lxml.html.fromstring(html_text)
		curr_questions = reap_questions(html)

		# If the test isn't done, prepare [post_args] for next page
		if len(curr_questions):
			# Verify test integrity
			if not all(item in def_questions.items() for item in curr_questions.items()):
				raise RuntimeError("Questions have changed. Answer cache is bad!")
			questions.update(curr_questions)

			# Assemble responses
			post_args = {'answer_' + str(key): answers[key] for key in curr_questions}

			# Print responses
			for num in sorted(curr_questions):
				print(str(num) + ":\t" + curr_questions[num] + "\n\t" + values[int(answers[num])] + '\n')

			submit_tag = html.find(".//input[@type='submit']")
			post_args["submit"] = submit_tag.value  # submit_tag.type == "submit"
			for tag in html.findall(".//input[@type='hidden']"):
				post_args[tag.name] = tag.value
			pageno = post_args["pageno"]
		else:
			post_args = None
			pageno = 'f'

		# with open('/Users/alex/Desktop/page' + pageno + ".html", "a+") as f:
			# f.write(html_text)

	h2 = html.find(".//h2")
	print(h2.text_content())

	lines = h2.text_content().split('\n')
	x = float(lines[0][-6:])
	y = float(lines[1][-6:])
	pyplot.scatter(x, y)
	pyplot.xlim(-10, 10)
	pyplot.ylim(-10, 10)
	pyplot.title("Political coordinates")
	pyplot.xlabel("Economic Left/Right")
	pyplot.ylabel("Social Libertarian/Authoritarian")
	pyplot.grid()
	pyplot.show()
	return questions


def main():
	compass()


if __name__ == '__main__':
	main()
