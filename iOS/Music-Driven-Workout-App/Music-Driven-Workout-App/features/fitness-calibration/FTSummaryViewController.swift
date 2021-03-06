//
//  FTSummaryViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class FTSummaryViewController: UIViewController {

    var viewModel = ViewModel()

    var category: String = ""
    var numEx: Int = 3
    var exChoices: [Int] = [Int]()
    var reply: [[String:Any]] = [[String:Any]]()
    var frequencies: [[String: Any]]!
    
    var exercises: [[String:Any]] = [[String:Any]]()
    var exerciseInfo = [String: Any]()
    var isCalibration: Bool = false
    var exNum: Int?
    
    @IBOutlet weak var tableView: UITableView?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print("user: \(global.userid)")

        let request = APIRequest()
        self.frequencies = [[String:Any]]()
        print(self.frequencies)
        print(exChoices, global.userid, category, numEx)
        var trackedStr: String = ""
        trackedStr = exChoices.map { String($0) }.joined(separator: ",")
        if trackedStr == "" {
            trackedStr = "144"
        }
        let qstr = "categories=\(category)&numexercises=\(numEx)&exerciseids=\(trackedStr)&key=SoftCon2018"
        request.submitPostServer(route: "/api/fitness/test/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = request.parseJsonRespone(data: data!)!
            self.exercises = self.reply
            self.exerciseInfo = self.exercises.removeFirst()
            
            let vmitems = self.reply.map { ViewModelItem(item: Model(title: $0["name"] as! String, data: $0)) }
            self.viewModel.setItems(items: vmitems)
            
            
            DispatchQueue.main.async {
                self.tableView?.register(CustomCell.nib, forCellReuseIdentifier: CustomCell.identifier)
                self.tableView?.dataSource = self.viewModel
                self.tableView?.delegate = self.viewModel
                self.tableView?.estimatedRowHeight = 100
                self.tableView?.rowHeight = UITableViewAutomaticDimension
                self.tableView?.allowsSelection = false
                self.tableView?.separatorStyle = .none
            }
         
            }.resume()
        
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /* Navigation */
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        if segue.destination is FTExDescViewController
        {
            let vc = segue.destination as? FTExDescViewController
            //data to send
            vc?.exercisesRemaining = exercises
            vc?.exerciseInfo = exerciseInfo
            vc?.isCalibration = isCalibration
            vc?.numExercises = numEx
            vc?.exerciseNum = numEx - exercises.count
            vc?.frequencies = frequencies
        }
    }

}
