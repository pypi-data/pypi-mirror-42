PYTHON ?= python

check : \
	glue_ligolw_ilwd_verify \
	iterutils_verify \
	lal_verify \
	ligolw_test01 \
	test_ligolw_array \
	test_ligolw_ligolw \
	test_ligolw_lsctables \
	test_ligolw_table \
	test_ligolw_tokenizer \
	test_ligolw_utils \
	test_ligolw_utils_segments
	@echo "All Tests Passed"

define printpassfail
	{ echo "Pass" ; true ; } || { echo "Fail" ; false ; }
endef

glue_ligolw_ilwd_verify :
	@echo "=== start glue_ligolw_ilwd_verify ===>"
	$(PYTHON) glue_ligolw_ilwd_verify.py && $(printpassfail)
	@echo "<=== end glue_ligolw_ilwd_verify ==="

iterutils_verify :
	@echo "=== start iterutils_verify ===>"
	$(PYTHON) iterutils_verify.py && $(printpassfail)
	@echo "<=== end iterutils_verify ==="

lal_verify :
	@echo "=== start lal_verify ===>"
	$(PYTHON) lal_verify.py && $(printpassfail)
	@echo "<=== end lal_verify ==="

ligolw_test01 :
	@echo "=== start ligolw_test01 ===>"
	# test reading array data from a file
	$(PYTHON) ligo_lw_test_01.py && $(printpassfail)
	@echo "<=== end ligolw_test01 ==="

test_ligolw_array :
	@echo "=== start test_ligolw_array ===>"
	$(PYTHON) test_ligolw_array.py && $(printpassfail)
	@echo "<=== end test_ligolw_array ==="

test_ligolw_ligolw :
	@echo "=== start test_ligolw_ligolw ===>"
	$(PYTHON) test_ligolw_ligolw.py && $(printpassfail)
	@echo "<=== end test_ligolw_ligolw ==="

test_ligolw_lsctables :
	@echo "=== start test_ligolw_lsctables ===>"
	$(PYTHON) test_ligolw_lsctables.py && $(printpassfail)
	@echo "<=== end test_ligolw_lsctables ==="

test_ligolw_table :
	@echo "=== start test_ligolw_table ===>"
	$(PYTHON) test_ligolw_table.py && $(printpassfail)
	@echo "<=== end test_ligolw_table ==="

test_ligolw_tokenizer :
	@echo "=== start test_ligolw_tokenizer ===>"
	$(PYTHON) test_ligolw_tokenizer.py && $(printpassfail)
	@echo "<=== end test_ligolw_tokenizer ==="

test_ligolw_utils :
	@echo "=== start test_ligolw_utils ===>"
	$(PYTHON) test_ligolw_utils.py && $(printpassfail)
	@echo "<=== end test_ligolw_utils ==="

test_ligolw_utils_segments :
	@echo "=== start test_ligolw_utils_segments ===>"
	$(PYTHON) test_ligolw_utils_segments.py && $(printpassfail)
	@echo "<=== end test_ligolw_utils_segments ==="

clean :
	rm -f ligo_lw_test_01*png
