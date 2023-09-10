#include <linux/list.h>

// 직접 리스트를 구현할 경우
struct cat {
    unsigned long tail_length; // 꼬리의 길이(cm)
    unsigned long weight; // 무게(kg)
    char *name; // 이름
    bool Is_cute; // 귀여운 고양이인가?
    struct cat *next; // 연결 리스트의 다음 항목
    struct cat *prev; // 연결 리스트의 이전 항목
};

/*
    2.1 커널 개발 과정에서 연결 리스트가 공식 구현이 도입
    모든 연결 리스트는 이 공식 구현 방법을 사용
    <linux/list.h> 헤더 파일에 정의
*/

// <linux/list.h>에 구현된 list
struct list_head
{
    struct list_head *next, *prev;
};

// 공식 리스트를 사용할 경우
struct cat {
    unsigned long tail_length; // 꼬리의 길이(cm)
    unsigned long weight; // 무게(kg)
    char *name; // 이름
    bool Is_cute; // 귀여운 고양이인가?
    struct list_head list; // cat 구조체 리스트
};
/*
    이렇게 구현할 경우 cat 구조체의 list.next는 다음 항목을 가리키고, list.prev는 이전 항목을 가리키게 할 수 있다.
    <linux/list.h>에 구현된 list_add()를 사용하면 기존 연결 리스트에 새로운 노드를 추가할 수 있다.
    이런 함수는 범용성을 갖추고 있다.
    list_head 구조체만을 대상으로 처리하기 때문이다.

    이렇게 구현된 cat 구조체에서 list는 다음 cat구조체가 아니라 해당 구조체의 list 필드를 가리킨다.
    따라서 다음 노드의 구조체에 접근 하기 위해서는 구조체에서 해당 list 필드의 offset(상대적 위치)을 알아낸 후,
    해당 offset을 통해 구조체가 시작하는 위치를 계산하여 접근 가능하다.
*/

// container_of() 매크로를 사용하면 특정 변수 항목을 가지고 있는 부모 구조체를 쉽게 찾아낼 수 있다.
// C에서는 구조체내 특정 변수의 상대적인 offset이 컴파일 시점에 ABI수준에서 고정되기 때문이다.
#define container_of(ptr, type, member) ({ \
    const typedef(((type *)0)->member) *__mptr = (ptr); \
    (type *)( (char *)__mptr - offsetof(type, member));})
// container_of() 매크로를 사용하면 list_head가 들어 있는 부모 구조체를 반환하는 함수를 간단하게 정의할 수 있다.

#define list_entry(ptr, type, member) \
    container_of(ptr, type, member)
// 커널은 list_entry() 를 비롯한 연결 리스트 생성, 조작 등의 관리 함수를 제공하며, 이런 함수는 list_head가 들어 있는 구조체에 상관없이 동작한다.

// 리스트는 사용하기 전에 초기화해야 한다.
// 대부분의 항목이 동적으로 생성되므로(이 때문에 연결 리스트를 사용할 것이다), 연결 리스트의 초기화는 실행 시에 처리하는 것이 일반적이다.
struct cat *black_cat;
black_cat = kmalloc(sizeof(*black_cat), GFP_KERNEL);
black_cat->tail_length = 30;
black_cat->weight = 6;
black_cat->name = "Ggam Bi";
black_cat->is_cute = true;
INIT_LIST_HEAD(black_cat->list);

// 정적으로 생성할 경우 다음과 같이 직접적인 방식으로 선언 가능
struct cat black_cat_directly
{
    .tail_length = 30,
    .weight = 6,
    .name = "Ggam Bi",
    .is_cute = true,
    .list = INIT_LIST_HEAD(black_cat->list),
};

// 전체 리스트를 가리키는 데 사용하는 헤드 포인터가 필요
// list_head 구조체가 연결 리스트 자체를 가리키는 데 사용하는 특별한 포인터 역할을 할 수 있다.
static LIST_HEAD(cat_list); // cat_list라는 이름의 list_head 구조체를 초기화한다.

/*
연결 리스트 조작

커널을 연결 리스트를 조작하는 함수를 제공
이런 함수는 하나 이상의 list_head 구조체 포인터를 인자로 받는다.
모든 함수는 C 인라인 함수로 구현되어 있으며, <linux/list.h> 파일에 들어 있다.
이런 함수는 모두 O(1) -> 리스트나 다른 입력의 크기에 상관없이 일정한 시간 안에 실행된다.
*/

// 연결 리스트에 노드 추가
list_add(struct list_head *new, struct list_head *head) // head 노드 바로 뒤에 new 노드를 추가한다.
// 일반적으로 환형 리스트에는 첫 번쨰나 마지막 노드라는 개념이 없으므로 head에 어떤 항목을 지정해도 상관 없다.
// '마지막' 항목을 전달한다면, 이 함수로 stack을 구현 가능

list_add(&new_cat->list, &cat_list); // cat_list에 새로운 struct cat(new_cat node)을 추가

// 연결 리스트의 마지막에 노드를 추가
list_add_tail(struct list_head *new, struct list_head *head); // head 노드 바로 앞에 new 노드를 추가
// list_add()와 마찬가지로 환형 리스트이므로 head에 어떤 항목을 지정해도 상관없다.
// '첫 번째' 항목을 전달한다면, 이 함수로 큐를 구현할 수 있다.

// 연결 리스트에서 노드 제거
list_del(struct list_head *entry); // 리스트에서 entry 항목을 제거
// 이 함수는 entry나 entry가 들어있는 구조체가 차지하고 있던 메모리를 해제하지 않는다.
// 이 함수는 해당 항목을 리스트에서 제거하는 동작만 수행
// 보통 이 함수를 호출한 다음 list_head와 list_head가 들어 있는 자료구조의 메모리를 해제해야 한다.

list_del(&new_cat->list); // cat_list에 추가한 cat 노드(new_cat)를 제거
// 함수의 파라미터에 fox_list가 없음
// 특정 노드만을 입력으로 받아 해당 노드의 이전 및 다음 노드의 포인터를 조정해 해당 노드를 리스트에서 제거한다.
static inline void __list_del(struct list_head *prev, struct list_head *next)
{
    next->prev = prev;
    prev->next = next;
}

static inline void list_del(struct list_head *entry)
{
    __list_del(entry->prev, entry->next);
}

list_del_init(struct list_head *entry); // 노드를 리스트에서 제외 후 해당 노드를 초기화
// 주어진 list head를 초기화한다는 점만 제외하면 list_del() 함수와 같다.
// 해당 항목을 리스트에서 제거해야 하지만 자료구조 자체는 재사용이 필요한 경우 사용

// 연결 리스트의 노드 이동과 병합
list_move(struct list_head *list, struct list_head *head); // 리스트에서 list 항목을 제거한 다음 head 항목 뒤에 추가

list_move_tail(struct list_head *list, struct list_head *head); // 리스트의 노드를 다른 리스트의 끝으로 이동
// 이 함수는 list_move() 와 같은 동작을 하지만 list 항목을 head 항목 앞에 추가한다.

list_enpty(struct list_head *head); // 리스트가 비어 있는지 확인
// 리스트가 비어 있으면 0이 아닌 값을 반환
// 비어 있지 않으면 0을 반환

list_splice(struct list_head *list, struct list_head *head); // 끊어져 있는 두 리스트를 합칠 경우
// list가 가리키는 노드를 head 앞에 추가하여 두 리스트를 병합한다.

// 끊어져 있는 두 리스트를 하나로 합치고 이전 리스트를 다시 초기화
list_splice_init(struct list_head *list, struct list_head *head);
// 빈 리스트가 되는 list를 다시 초기화한다는 점만 제외하면 list_splic()와 같다.

/*
연결 리스트 탐색

n개의 항목을 가진 연결 리스트의 모든 항목을 탐색하는 작업의 복잡도 : O(n)
*/

// 리스트 탐색 기본 방법
struct list_head *p;

list_for_each(p, cat_list) {
    // p는 리스트의 항목을 가리킨다
}
// 리스트 구조체를 가리키는 포인터는 큰 의미가 없다.
// 중요한 값은 list_headㅏ 들어 있는 부모 구조체(cat)의 포인터이다.
// 앞에서 살펴본 list_entry() 매크로를 이용하면 list_head가 들어 있는 구조체를 얻을 수 있다.

struct list_head *p;
struct cat *c;

list_for_each(p, cat_list) {
    // c는 리스트가 들어 있는 cat 구조체를 가리킨다.
    c = list_entry(p, struct cat, list);

}

// 실제로 사용하는 방식
list_for_each_entry(pos, head, member);
// pos : list_head가 들어 있는 객체를 가리키는 포인터, list_entry() 함수의 반환값
// head : 탐색을 시작하려는 리스트 노드의 list_head를 가리키는 포인터

struct cat *c;

list_for_each_entry(c, &cat_list, list) {
    // 루프가 반복될 때마다 'c'는 다음 cat 구조체를 가리킨다.
}

// 실제 사용 예 : 커널 파일 시스템 알림 모듈 - inotify
static struct inotify_watch *inode_find_handle(struct inode *inode, struct inotify_handle *ih)
{
    struct inotify_watch *watch;

    list_for_each_entry(watch, &inode->inotify_watches, i_list) {
        if (watch->ih == ih)
            return watch;
    }

    return NULL;
}
/*
    indoe->inotify_watches 리스트의 모든 항목을 탐색
    리스트의 각 항목은 struct inotify_watch 자료구조로 구성
    이 안에는 i_list라는 이름으로 list_head 구조체가 들어 있다.
    루프가 반복될 때마다 watchㅇ 포인터는 리스트의 다음 노드를 가리킨다.
    이 함수의 목적은 주어진 inode 구조체의 inotify_watches 리스트에서 주어진 핸들과 일치하는 핸들을 가진 inotify_watch 항목을 찾는 것
*/

// 역방향으로 리스트 탐색
list_for_each_entry_reverse(pos, head, member);
// 역순으로 탐색한다는 점을 제외하면, list_for_each_entry() 매크로와 동일하게 동작
// next 포인트를 따라가며 앞 방향으로 리스트를 지나가는 대신 prev 포인터를 따라 역방향으로 진행
// 1. 찾으려는 항목이 탐색 시작위치의 뒤편에 있다는 사실을 알고 있을 경우 역방향으로 탐색하면 빨리 찾을 수 있다.
// 2. LIFO 방식을 구현할 수 있다.
// 역방향으로 이동할 이유가 분명하지 않을 경우 list_for_each_entry() 매크로 사용을 권장

/*
제거하면서 탐색

리스트를 탐색하면서 항목을 제거하는 경우 기본 리스트 탐색 방법이 부적합
기본 탐색 방법은 리스트의 항목이 변경되지 않는다고 가정하므로 루프를 실행하는 도중에 현재 항목이 제거되면 이후에는 다음(또는 이전) 포인터를 따라 진행할 수 없다.
다음(또는 이전) 포인터를 제거하기 전에 임시 변수에 저장해 두는 방식으로 문제를 해결
*/
list_for_each_entry_safe(pos, next, head, member);
// pos와 형이 같은 next 포인터를 제공하는다는 점을 제외하면 list_for_each_entry()와 같은 방식으로 사용 가능
// next 포인터에 리스트의 다음 항목을 저장해 현재 항목을 제거해도 문제가 없다.

// 실제 사용 예 : inotify
void inotify_inode_is_dead(struct inode *inode)
{
    struct inotify_watch *watch, *next;

    mutex_lock(&inode->inotify_mutext);
    list_for_each_entry_safe(watch, next, &inode->inotify_watches, i_list)
    {
        struct inotify_handle *ih = watch->ih;
        mutex_lock(&ih->mutex);
        inotify_remove_watch_locked(ih, watch); // watch를 제거
        mutex_unlock(&ih->mutex);
    }
    mutex_unlock(&inode->inotify_mutex);
}
// inotify_wtches 리스트를 탐색하면서 모든 항목을 제거
// 역방향으로 리스트를 탐색하면서 제거할 경우
list_for_each_entry_safe_reverse(pos, n, head, member);
// 다른 코드에서 동시에 제거되거나, 어떤 형태로든 리스트가 동시에 조작될 수 있는 상황이라면 리스트에 잠금을 걸어 접근을 제한해야 한다.