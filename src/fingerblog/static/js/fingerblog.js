function goTop(acceleration, time) {
	acceleration = acceleration || 0.1;//加速度 acceleration
	time = time || 15;//时间间隔
	var x=0,y=0;
			
	if (document.documentElement) {
		x = document.documentElement.scrollLeft|| 0;
		y = document.documentElement.scrollTop || 0;
	}
			
	var speed = 1 + acceleration;//滚动速度
	//  floor()返回值为小于等于其数值参数的最大整数值 假如 y=36 speed=1.1   36/1.1=32;
	// scrollTo()滚动条将要移动到x y 经过计算得出的值
	window.scrollTo(Math.floor(x / speed), Math.floor(y / speed));
	//如果 x (scrollLeft!=0)||y(scrollTop!=0)还未移动到顶部.所以setTimeout()继续执行该函数
	if(x > 0 || y > 0) {
		var invokeFunction = "goTop(" + acceleration + ", " + time + ")";
		window.setTimeout(invokeFunction, time);
	}
}