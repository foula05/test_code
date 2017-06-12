section_three:
	python section3/section3_code.py data/data.csv y

section_one:
	python section1/section1_code.py 3 data/data.csv

clean:
	rm -rf ~* section1/~. section2/~. section3/~. lala*
