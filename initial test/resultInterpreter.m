

% used to produce plots from results of the cp optimiser
% 
DownLink = readmatrix("Communications Data log.csv");
DataIn = readmatrix('Chosen Actions.csv');
DataValue = readmatrix('Avg objects Detection log.csv');
tspan =length(DataIn);
Aspan = length(DataIn(1,:));

tvect = linspace(0,86400*20,tspan);
observing  = zeros(tspan,1);
value = zeros(tspan,1);
storedData_Log = zeros(tspan,1);

maxStorage = 5000;
DataperObs = 25;%29.73e3; % data produced per observation
Downlinkrate = 250;%250e3; % data downlinked per second during communications
storedData = 0;



for t = 1:tspan
    if sum(DataIn(t,1:Aspan-1)) > 0 
        observing(t) = 1;
        value(t) = max(DataValue(t,:))*observing(t);
        storedData = storedData + DataperObs; 
    end
    
    if DownLink(t) == 1
        storedData = storedData - Downlinkrate;

    end

    storedData_Log(t) = storedData;


    if t/1000 == ceil(t/1000)
    disp( t )
    disp("steps completed of ") 
    disp(tspan)
    end

end

disp('succesfully exited loop')

    temp = sum(value);
    string = 'total value downlinked';
    X = [string, num2str(temp)];
    disp(X)



figure(1)

plot(tvect(1:tspan)/86400, observing(1:tspan), 'color', 'green')


figure(2)
bar(tvect(1:tspan), value(1:tspan))

figure(3)
plot(tvect(1:tspan)/86400, storedData_Log(1:tspan) , 'Color' , 'blue')
hold on 
yline(5000,'Color','red')
hold off


value = value.* 1/max(value);
storedData_Log = storedData_Log .* 1/max(storedData_Log);

figure(4)
plot(tvect(1:tspan)/86400,storedData_Log(1:tspan))
hold on 
plot(tvect(1:tspan)/86400,value(1:tspan))
legend('stored data','value of stored data')
hold off


figure(5)
plot(tvect(1:tspan)/86400,value(1:tspan))
hold on
plot(tvect(1:tspan)/86400,-1*observing(1:tspan))
legend('Value of observed data','observing')
hold off


