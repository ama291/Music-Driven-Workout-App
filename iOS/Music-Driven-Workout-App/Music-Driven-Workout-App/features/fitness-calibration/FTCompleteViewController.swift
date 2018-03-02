//
//  FTCompleteViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class FTCompleteViewController: UIViewController {
    var viewModel = ViewModel()

    @IBOutlet weak var tableView: UITableView!
    var userid: String!
    var exerciseName: String!
    var isCalibration: Bool!
    var frequencies: [[String:Any]]!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print("user: \(userid)")

        print(self.frequencies, "frequencies")
        var freq: String = ""
        freq = String(describing: self.frequencies![0]["frequency"]! as! Float)
        let name: String = self.frequencies![0]["name"]! as! String
        print(freq, name)
        print("\(name): \(freq)")
        
        let vmitems = self.frequencies!.map { ViewModelItem(item: Model(title: "\($0["name"]! as! String): \($0["frequency"]! as! Float) RPM" , data: $0)) }
        print(vmitems[0].title)
        self.viewModel.setItems(items: vmitems)
        
        self.tableView?.register(CustomCell.nib, forCellReuseIdentifier: CustomCell.identifier)
        self.tableView?.dataSource = self.viewModel
        self.tableView?.delegate = self.viewModel
        self.tableView?.estimatedRowHeight = 100
        self.tableView?.rowHeight = UITableViewAutomaticDimension
        self.tableView?.allowsSelection = false
        self.tableView?.separatorStyle = .none
        
        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    /*
     // MARK: - Navigation
     
     // In a storyboard-based application, you will often want to do a little preparation before navigation
     override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
     // Get the new view controller using segue.destinationViewController.
     // Pass the selected object to the new view controller.
     }
     */
    @IBAction func goToHome(_ sender: UIButton) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        vc.userid = userid!
        present(vc, animated: true, completion: nil)
    }
    
}

