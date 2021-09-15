

```go

package main

import (
	"fmt"
)

func hiddenTransform() *int {
	return nil
}

func main() {

	// nil（无类型）和空接口拥有相同的底层数据，类型和值都是<nil>
	fmt.Printf("type: %T, value: %v \n", nil, nil)
	var i interface{}
	fmt.Printf("type: %T, value: %v \n", i, i)
	println(i)
	if i == nil {
		fmt.Printf("check empty interface equal nil with same type and value.\n")
	}

	// 隐式转换，空接口承载具体类型后类型信息就不是<nil>，虽然值还是<nil>
	i = hiddenTransform()
	fmt.Printf("type: %T, value: %v \n", i, i)
	println(i)
	if i == nil {
		fmt.Printf("check equal again\n")
	}

	// 此时判空因为类型导致不为空绕过检查，而方法是固定的函数指针地址肯定能够访问到。
	// 访问类型的内部变量时没有实例可用于寻址导致panic

	// 所以接口调用方法的时候需要确认值是有效的，这是很繁琐的体验。
	// 最好的方式是获取接口的地方无效时直接返回nil便于检查，带类型不带值的接口干不了啥事情
	// 这跟C++的空指针调用成员函数一样，如果不访问成员只做编译器确定的事情确实不会出问题
}

```

