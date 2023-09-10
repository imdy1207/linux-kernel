// 연결 리스트의 데이터 항목
struct list_element {
    void *data; // 항목에 담긴 데이터(payload)
    struct list_element *next; // 다음 항목을 가리키는 포인터
};

// 연결 리스트의 데이터 항목
struct list_element {
    void *data; // 항목에 담긴 데이터(payload)
    struct list_element *next; // 다음 항목을 가리키는 포인터
    struct list_element *prev;  // 이전 항목을 가리키는 포인터
};

// 마지막 노드의 next가 head를 가리킨다