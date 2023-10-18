// 연결 리스트의 데이터 항목
struct list_element {
    void *data; // 항목에 담긴 데이터(payload)
    struct list_element *next; // 다음 항목을 가리키는 포인터
};