		.text
min_int:
		mov		4(%esp), %eax
		mov		8(%esp), %ecx
		cmp		%ecx, %eax
		jle 	return
		mov		%ecx, %eax
return:
		ret


		.global build
build:
		push	%ebp
		mov		%esp, %ebp
		push 	%ebx
		/*	%eax, %ecx, %edx
			8 - *t
			12 - *ar
			16 - v
			20 - tl
			24 - tr
		*/
		mov		24(%ebp), %ecx
		sub		20(%ebp), %ecx
		sub		$1, %ecx
		jnz		else
		mov		8(%ebp), %eax
		mov		16(%ebp), %edx
		mov		12(%ebp), %ecx
		mov		20(%ebp), %ebx
		push	%esi
		mov		(%ecx, %ebx, 4), %esi
		mov	    %esi, (%eax, %edx, 4)
		pop		%esi
		pop		%ebx
		pop		%ebp
		ret
else:
		push	%edi
		mov		16(%ebp) ,%edi
		add		%edi, %edi
		inc		%edi
		mov		20(%ebp), %ebx
		add		24(%ebp), %ebx
		shr		$1, %ebx
		// cleared
		push	%ebx
		push	20(%ebp)
		push	%edi
		push	12(%ebp)
		push	8(%ebp)
		call	build
		add		$20, %esp

		push	24(%ebp)
		push	%ebx
		inc		%edi
		push	%edi
		push	12(%ebp)
		push	8(%ebp)
		call	build
		add		$20, %esp

		mov		8(%ebp), %eax
		push	(%eax, %edi, 4)
		dec		%edi
		push	(%eax, %edi, 4)
		call 	min_int
		add		$8, %esp
		mov		16(%ebp), %edi
		mov		8(%ebp), %ecx
		mov		%eax, (%ecx, %edi, 4)

		pop		%edi
		pop		%ebx
		pop		%ebp
		ret




		.global set_value
set_value:
		/*
			8 - val
			12 - ind
			16 - *t
			20 - v
			24 - tl
			28 - tr
		*/
		push 	%ebp
		mov		%esp, %ebp

		mov		28(%ebp), %eax
		sub		24(%ebp), %eax
		sub		$1,	%eax
		jnz		else1
		mov		8(%ebp), %eax
		mov		16(%ebp), %ecx
		mov		20(%ebp), %edx
		mov		%eax, (%ecx, %edx, 4)
		pop		%ebp
		ret
else1:
		push	%edi
		push	%ebx
		mov		20(%ebp), %ebx
		add		%ebx, %ebx
		inc		%ebx
		mov		28(%ebp), %edi
		add		24(%ebp), %edi
		shr		$1, %edi
		cmp		12(%ebp), %edi
		jle		cond

		push	%edi
		push	24(%ebp)
		push	%ebx
		push	16(%ebp)
		push	12(%ebp)
		push	8(%ebp)
		call	set_value
		add		$24, %esp

		jmp 	fin
cond:

		inc		%ebx
		push	28(%ebp)
		push	%edi
		push	%ebx
		push	16(%ebp)
		push	12(%ebp)
		push	8(%ebp)
		call	set_value
		add		$24, %esp

fin:

		mov		16(%ebp), %eax
		mov		20(%ebp), %ebx
		add		%ebx, %ebx
		inc		%ebx
		push	(%eax, %ebx, 4)
		inc 	%ebx
		push	(%eax, %ebx, 4)
		call	min_int
		add		$8, %esp

		mov		16(%ebp), %ecx
		mov		20(%ebp), %edx
		mov		%eax, (%ecx, %edx, 4)

		pop		%ebx
		pop		%edi
		pop		%ebp
		ret




		.global get_min
get_min:
		/*
			8 - l
			12 - r
			16 - *t
			20 - v
			24 - tl
			28 - tr
		*/
		push	%ebp
		mov		%esp, %ebp

		mov		8(%ebp), %eax
		mov		24(%ebp), %ecx
		cmp		%eax, %ecx
		jl		after
		mov		12(%ebp), %eax
		mov		28(%ebp), %ecx
		cmp		%eax, %ecx
		jg		after

		mov		16(%ebp), %ecx
		mov		20(%ebp), %edx
		mov		(%ecx, %edx, 4), %eax
		pop 	%ebp
		ret

after:

		mov		8(%ebp), %eax
		mov		28(%ebp), %ecx
		cmp		%eax, %ecx
		jle		ret1 // tr <= l

		mov		12(%ebp), %eax
		mov		24(%ebp), %ecx
		cmp		%eax, %ecx
		jge		ret1
		jmp		els
ret1:
		mov		$2000000000, %eax
		pop		%ebp
		ret
els:
		push	%ebx
		mov		28(%ebp), %ebx
		add		24(%ebp), %ebx
		shr		$1, %ebx
		push	%edi
		mov		20(%ebp), %edi
		add		%edi, %edi
		inc		%edi

		push	%ebx
		push	24(%ebp)
		push	%edi
		push	16(%ebp)
		push	12(%ebp)
		push	8(%ebp)
		call	get_min
		add		$24, %esp
		push	%eax

		push	28(%ebp)
		push	%ebx
		inc		%edi
		push	%edi
		push	16(%ebp)
		push	12(%ebp)
		push	8(%ebp)
		call	get_min
		add		$24, %esp
		push	%eax

		call	min_int
		add		$8, %esp

		pop		%edi
		pop		%ebx
		pop		%ebp
		ret


#define MAXN 600000
		.data
i:
		.int 0
j:
		.int 0
T:
		.zero MAXN * 16
arr:
		.zero MAXN * 4
n:
		.int 0
q:
		.int 0
min_str:
		.asciz "min"
str:
		.asciz "228"
in_str:
		.asciz "%s"
in_int:
		.asciz "%d"
out_int:
		.asciz "%d\n"

		.text
		.global main
main:
		push	$n
		push	$in_int
		call	scanf
		add		$8, %esp
		xor	%ebx, %ebx
read_loop:
		cmp		%ebx, (n)
		je 		next
		lea		arr(, %ebx, 4), %edx
		push	%edx
		push	$in_int
		call	scanf
		add		$8, %esp
		inc		%ebx
		jmp		read_loop
next:
		push	(n)
		push	$0
		push	$0
		push	$arr
		push	$T
		call	build
		add		$20, %esp
next_loop:
		push	$str
		push	$in_str
		call	scanf
		add		$8, %esp
		cmp		$-1, %eax
		je		fn

		push	$i
		push	$in_int
		call	scanf
		add		$8, %esp
		mov		(i), %eax
		dec		%eax
		mov		%eax, (i)

		push	$j
		push	$in_int
		call	scanf
		add		$8, %esp

		mov		(str), %dl
		cmp		(min_str), %dl
		jne		set

		push	(n)
		push	$0
		push	$0
		push	$T
		push	(j)
		push	(i)
		call	get_min
		push	%eax
		push	$out_int
		call	printf
		add		$32, %esp

		jmp 	next_loop
set:

		push	(n)
		push	$0
		push	$0
		push	$T
		push	(i)
		push	(j)
		call	set_value
		add		$24, %esp

		jmp		next_loop

fn:
		mov		$0, %eax
		ret
// void build(*t, *ar, v, tl, tr)
// set_value(val, ind, *t, v, tl, tr)
// get_min(l, r, *t, v, tl, tr)

/*
5
1 2 3 4 5
min 2 5
min 1 5
min 1 4
min 2 4
set 1 10
set 2 3
set 5 2
min 2 5
min 1 5
min 1 4
min 2 4
*/