//
//  ViewController.swift
//  Accl
//
//  Created by Lucy Newman on 2/4/18.
//  Copyright © 2018 Lucy Newman. All rights reserved.
//

import UIKit
import CoreMotion

class ViewController: UIViewController {
    
    var motionManager = CMMotionManager()
    var motionData: [[String : Double]] = []
    
    var timer = Timer()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func viewDidAppear(_ animated: Bool) {
        timer = Timer.scheduledTimer(timeInterval: 30, target: self, selector: #selector(ViewController.printResult), userInfo: nil, repeats: false)
        
        motionManager.accelerometerUpdateInterval = 0.2
        
        motionManager.startAccelerometerUpdates(to: OperationQueue.current!) {(data, error) in
            if let myData = data
            {
                var myDict: [String: Double] = [:]
                myDict = ["x": myData.acceleration.x, "y": myData.acceleration.y, "z": myData.acceleration.z, "timestamp": myData.timestamp]
                
                self.motionData.append(myDict)
                
            }
        }
    }
    
    @objc func printResult() {
        //        print(self.motionData)
        
        let encoder = JSONEncoder()
        encoder.outputFormatting = .prettyPrinted
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: self.motionData, options: .prettyPrinted)
            let decoded = try JSONSerialization.jsonObject(with: jsonData, options: [])
            print(decoded)
        }
        catch {
            print(error.localizedDescription)
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
}

