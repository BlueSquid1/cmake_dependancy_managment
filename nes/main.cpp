#include <iostream>

#include <cpu.h>
#include <gpu.h>

int main()
{
	Cpu cpu;
	cpu.start_cpu();

	Gpu gpu;
	gpu.start_gpu();
	std::cout << "nes started\n";
	return 0;
}