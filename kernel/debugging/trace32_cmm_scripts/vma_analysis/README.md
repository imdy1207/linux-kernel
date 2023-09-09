task_struct → mm_struct → vm_area_struct → mm_struct → task_struct 순으로 참조해 나가며 데이터를 모니터링 및 분석 하고 각 구조체 필드들의 주요 필드를 이해
vm_area_struct와 mm_struct, task_struct의 관계를 자료구조를 통해 확인

task_struct(task descriptor) - 프로세스의 값을 담고 있는 구조체
mm_struct(memoru descriptor) - 프로세스의 메모리 정보를 담고 있는 구조체
vm_area_struct(VMA) - 가상메모리 공간의 정보를 담고 있는 구조체
